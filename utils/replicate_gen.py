#!/usr/bin/env python3
"""
Replicate API wrapper for Full Pack Generator.
Three-tier model cascade:
  1. google/nano-banana-2       (primary — 10 consecutive failures to escalate)
  2. google/nano-banana-pro     (secondary — 10 consecutive failures to escalate)
  3. black-forest-labs/flux-2-flex (last resort — permanent)
"""

import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path

API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")
BASE_URL = "https://api.replicate.com/v1"

# Model cascade (order matters)
MODEL_CASCADE = [
    "google/nano-banana-2",
    "google/nano-banana-pro",
    "black-forest-labs/flux-2-flex",
]
FALLBACK_THRESHOLD = 10  # consecutive failures per model before escalating

# State tracking
_current_model_index = 0
_consecutive_failures = 0

# Google UAC target sizes
UAC_SIZES = {
    "landscape": {"w": 1200, "h": 628, "aspect": "16:9"},
    "square":    {"w": 1200, "h": 1200, "aspect": "1:1"},
    "portrait":  {"w": 1200, "h": 1500, "aspect": "4:5"},
    "native":    {"w": 1200, "h": 627, "aspect": "16:9"},
}

FLUX_ASPECT_MAP = {
    "16:9": "16:9", "1:1": "1:1", "4:5": "4:5",
    "9:16": "9:16", "3:2": "3:2", "2:3": "2:3",
}
FLUX_RESOLUTION_MAP = {"1K": "1 MP", "2K": "2 MP", "4K": "4 MP"}

# Model name shortcuts for CLI
MODEL_SHORTCUTS = {
    "nano": "google/nano-banana-2",
    "nano-pro": "google/nano-banana-pro",
    "flux": "black-forest-labs/flux-2-flex",
    "auto": None,
}


def _headers():
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }


def _current_model():
    return MODEL_CASCADE[_current_model_index]


def _is_flux(model):
    return "flux" in model


def _is_google(model):
    return model.startswith("google/")


def upload_file(filepath):
    """Upload a local file to Replicate's file hosting. Returns a URL."""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    fname = Path(filepath).name
    mime = "image/png" if fname.endswith(".png") else "image/jpeg"
    with open(filepath, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/files",
            headers=headers,
            files={"content": (fname, f, mime)},
        )
    if resp.status_code in (200, 201):
        data = resp.json()
        return data.get("urls", {}).get("get") or data.get("url")
    print(f"Upload failed ({resp.status_code}): {resp.text}", file=sys.stderr)
    return None


def _build_payload(model, prompt, aspect_ratio, resolution, output_format, image_input):
    """Build the correct payload for a given model."""
    if _is_flux(model):
        payload = {
            "prompt": prompt,
            "aspect_ratio": FLUX_ASPECT_MAP.get(aspect_ratio, aspect_ratio),
            "resolution": FLUX_RESOLUTION_MAP.get(resolution, "1 MP"),
            "output_format": "jpg" if output_format == "jpg" else output_format,
            "output_quality": 90,
            "safety_tolerance": 5,
            "prompt_upsampling": True,
        }
        if image_input:
            payload["input_images"] = image_input if isinstance(image_input, list) else [image_input]
    else:
        # Google models (nano-banana-2, nano-banana-pro)
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "output_format": output_format,
        }
        if image_input:
            payload["image_input"] = image_input
    return payload


def _try_create(model, prompt, aspect_ratio, resolution, output_format, image_input):
    """Try to create a prediction on a specific model. Returns (result, error)."""
    payload = _build_payload(model, prompt, aspect_ratio, resolution, output_format, image_input)
    try:
        resp = requests.post(
            f"{BASE_URL}/models/{model}/predictions",
            headers=_headers(),
            json={"input": payload},
            timeout=30,
        )
        if resp.status_code in (200, 201):
            result = resp.json()
            result["_model_used"] = model
            return result, None
        else:
            return None, f"HTTP {resp.status_code}: {resp.text[:200]}"
    except requests.exceptions.Timeout:
        return None, "Request timeout"
    except Exception as e:
        return None, str(e)


def create_prediction(prompt, aspect_ratio="1:1", resolution="1K",
                      output_format="jpg", image_input=None, model=None):
    """
    Create a prediction on Replicate with three-tier cascade fallback.

    Auto mode (model=None):
    - Starts with google/nano-banana-2
    - After 10 consecutive failures, escalates to google/nano-banana-pro
    - After 10 more consecutive failures, escalates to black-forest-labs/flux-2-flex
    - If the current model succeeds, the failure counter resets (but model tier stays)
    - Once escalated, does NOT go back to previous tiers
    """
    global _current_model_index, _consecutive_failures

    # Explicit model requested — no cascade logic
    if model:
        result, err = _try_create(model, prompt, aspect_ratio, resolution, output_format, image_input)
        if result:
            return result
        print(f"  [{model}] Failed: {err}", file=sys.stderr)
        return None

    # Auto mode — use cascade
    current = _current_model()
    result, err = _try_create(current, prompt, aspect_ratio, resolution, output_format, image_input)

    if result:
        if _consecutive_failures > 0:
            print(f"  [{current}] Recovered after {_consecutive_failures} failures")
        _consecutive_failures = 0
        return result

    # Failed
    _consecutive_failures += 1
    is_last = _current_model_index >= len(MODEL_CASCADE) - 1
    remaining = FALLBACK_THRESHOLD - _consecutive_failures

    print(f"  [{current}] Failed ({_consecutive_failures}/{FALLBACK_THRESHOLD}): {err}", file=sys.stderr)

    if _consecutive_failures >= FALLBACK_THRESHOLD and not is_last:
        # Escalate to next model
        _current_model_index += 1
        _consecutive_failures = 0
        next_model = _current_model()
        print(f"  >>> ESCALATING to {next_model} after {FALLBACK_THRESHOLD} consecutive failures", file=sys.stderr)

        # Retry immediately with the next model
        result, err = _try_create(next_model, prompt, aspect_ratio, resolution, output_format, image_input)
        if result:
            return result
        print(f"  [{next_model}] Also failed: {err}", file=sys.stderr)
        _consecutive_failures = 1  # Count this as first failure on new model
        return None

    if not is_last:
        print(f"  Keeping {current} — {remaining} failures before escalation", file=sys.stderr)
    return None


def poll_prediction(prediction_id, timeout=300):
    """Poll until a prediction completes. Returns output URL or None."""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = requests.get(f"{BASE_URL}/predictions/{prediction_id}", headers=headers, timeout=15)
            data = resp.json()
            status = data.get("status")
            if status == "succeeded":
                output = data.get("output")
                if isinstance(output, list):
                    return output[0] if output else None
                return output
            if status in ("failed", "canceled"):
                print(f"Prediction {prediction_id} {status}: {data.get('error')}", file=sys.stderr)
                return None
        except Exception as e:
            print(f"  Poll error: {e}", file=sys.stderr)
        time.sleep(2)
    print(f"Timeout polling {prediction_id}", file=sys.stderr)
    return None


def download_image(url, filepath):
    """Download an image from URL to filepath."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, stream=True, timeout=60)
    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
    return filepath


def resize_uac(filepath, size_key):
    """Resize image to exact UAC dimensions using sips (macOS)."""
    spec = UAC_SIZES.get(size_key)
    if not spec:
        return filepath
    w, h = spec["w"], spec["h"]
    subprocess.run(["sips", "-z", str(h), str(w), filepath], capture_output=True)
    return filepath


def generate_one(prompt, filepath, aspect_ratio="1:1", resolution="1K",
                 image_input=None, uac_size=None, model=None):
    """Generate a single image: create -> poll -> download -> resize."""
    pred = create_prediction(prompt, aspect_ratio, resolution,
                             image_input=image_input, model=model)
    if not pred:
        return None

    model_used = pred.get("_model_used", "unknown")
    url = poll_prediction(pred["id"])
    if not url:
        return None

    download_image(url, filepath)
    if uac_size:
        resize_uac(filepath, uac_size)
    print(f"  Generated: {Path(filepath).name} [{model_used}]")
    return filepath


def batch_generate(jobs, model=None):
    """
    Generate multiple images efficiently.

    jobs: list of dicts with: prompt, filepath, aspect_ratio, resolution, image_input, uac_size
    Returns list of successfully saved filepaths.
    """
    active = []
    for i, job in enumerate(jobs):
        pred = create_prediction(
            prompt=job["prompt"],
            aspect_ratio=job.get("aspect_ratio", "1:1"),
            resolution=job.get("resolution", "1K"),
            image_input=job.get("image_input"),
            model=model,
        )
        if pred:
            active.append({
                "id": pred["id"],
                "filepath": job["filepath"],
                "uac_size": job.get("uac_size"),
                "model": pred.get("_model_used", "unknown"),
            })
            name = Path(job["filepath"]).stem
            print(f"  [{i+1}/{len(jobs)}] Created -> {name} [{pred.get('_model_used', '?')}]")
        else:
            print(f"  [{i+1}/{len(jobs)}] FAILED to create prediction", file=sys.stderr)
        time.sleep(0.3)

    print(f"\nPolling {len(active)} predictions...")
    results = []
    pending = list(active)
    start = time.time()

    while pending and (time.time() - start) < 600:
        still_pending = []
        for p in pending:
            try:
                headers = {"Authorization": f"Bearer {API_TOKEN}"}
                resp = requests.get(f"{BASE_URL}/predictions/{p['id']}", headers=headers, timeout=15)
                data = resp.json()
                status = data.get("status")
                if status == "succeeded":
                    output = data.get("output")
                    url = output[0] if isinstance(output, list) else output
                    if url:
                        download_image(url, p["filepath"])
                        if p.get("uac_size"):
                            resize_uac(p["filepath"], p["uac_size"])
                        results.append(p["filepath"])
                        print(f"  OK {Path(p['filepath']).name} [{p['model']}]")
                    else:
                        print(f"  FAIL {Path(p['filepath']).name}: no output URL")
                elif status in ("failed", "canceled"):
                    print(f"  FAIL {Path(p['filepath']).name}: {data.get('error', 'unknown')[:100]}")
                else:
                    still_pending.append(p)
            except Exception as e:
                print(f"  Poll error for {p['id']}: {e}", file=sys.stderr)
                still_pending.append(p)
        pending = still_pending
        if pending:
            time.sleep(2)

    if pending:
        print(f"\n  WARNING: {len(pending)} predictions still pending after timeout")
    return results


def get_status():
    """Return current cascade status for diagnostics."""
    return {
        "cascade": MODEL_CASCADE,
        "current_model": _current_model(),
        "current_tier": _current_model_index + 1,
        "consecutive_failures": _consecutive_failures,
        "threshold_per_tier": FALLBACK_THRESHOLD,
    }


# -- CLI ----------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate images with Replicate (3-tier model cascade)"
    )
    sub = parser.add_subparsers(dest="command")

    gen = sub.add_parser("generate", help="Generate a single image")
    gen.add_argument("prompt")
    gen.add_argument("-o", "--output", default="output.jpg")
    gen.add_argument("-a", "--aspect", default="1:1")
    gen.add_argument("-r", "--resolution", default="1K")
    gen.add_argument("-i", "--image", action="append", help="Reference image URL(s)")
    gen.add_argument("--uac", choices=["landscape", "square", "portrait", "native"])
    gen.add_argument("--model", choices=["nano", "nano-pro", "flux", "auto"], default="auto",
                     help="Model: nano, nano-pro, flux, or auto (cascade with 10-failure threshold)")

    batch_cmd = sub.add_parser("batch", help="Batch generate from JSON file")
    batch_cmd.add_argument("json_file")
    batch_cmd.add_argument("--model", choices=["nano", "nano-pro", "flux", "auto"], default="auto")

    up = sub.add_parser("upload", help="Upload a file to Replicate")
    up.add_argument("filepath")

    sub.add_parser("status", help="Show cascade status")

    args = parser.parse_args()

    if not API_TOKEN and args.command != "status":
        print("ERROR: Set REPLICATE_API_TOKEN environment variable", file=sys.stderr)
        sys.exit(1)

    if args.command == "generate":
        model = MODEL_SHORTCUTS.get(getattr(args, "model", "auto"))
        result = generate_one(
            args.prompt, args.output, args.aspect, args.resolution,
            image_input=args.image, uac_size=args.uac, model=model,
        )
        if result:
            print(f"Saved: {result}")
        else:
            sys.exit(1)

    elif args.command == "batch":
        model = MODEL_SHORTCUTS.get(getattr(args, "model", "auto"))
        with open(args.json_file) as f:
            jobs = json.load(f)
        results = batch_generate(jobs, model=model)
        print(f"\nDone: {len(results)}/{len(jobs)} images generated")

    elif args.command == "upload":
        url = upload_file(args.filepath)
        if url:
            print(url)
        else:
            sys.exit(1)

    elif args.command == "status":
        print(json.dumps(get_status(), indent=2))

    else:
        parser.print_help()
