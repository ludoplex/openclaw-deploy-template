"""Vocal isolation using demucs, loading/saving with soundfile to avoid torchcodec."""
import torch, soundfile as sf, numpy as np
from pathlib import Path
from demucs.pretrained import get_model
from demucs.apply import apply_model

OUT_DIR = Path(r"C:\Users\user\.openclaw\workspace\peridot-voice\separated")
OUT_DIR.mkdir(parents=True, exist_ok=True)

model = get_model("htdemucs")
model.eval()

files = [
    r"C:\Users\user\.openclaw\workspace\peridot-voice\quotes_all_time.wav",
    r"C:\Users\user\.openclaw\workspace\peridot-voice\once_said.wav",
    r"C:\Users\user\.openclaw\workspace\peridot-voice\makes_funny.wav",
]

for fpath in files:
    name = Path(fpath).stem
    print(f"Processing {name}...")
    
    # Load with soundfile (returns (samples, channels), sr)
    data, sr = sf.read(fpath, dtype='float32')
    
    # Convert to torch tensor (channels, samples)
    if data.ndim == 1:
        wav = torch.from_numpy(data).unsqueeze(0)
    else:
        wav = torch.from_numpy(data.T)
    
    # Resample if needed
    if sr != model.samplerate:
        import torchaudio
        wav = torchaudio.functional.resample(wav, sr, model.samplerate)
        sr = model.samplerate
    
    # Ensure stereo
    if wav.shape[0] == 1:
        wav = wav.repeat(2, 1)
    
    # Normalize
    ref = wav.mean(0)
    wav_norm = (wav - ref.mean()) / ref.std()
    
    # Apply model
    with torch.no_grad():
        sources = apply_model(model, wav_norm[None], device="cpu", progress=True)
    sources = sources * ref.std() + ref.mean()
    
    # Extract vocals
    vocal_idx = model.sources.index("vocals")
    vocals = sources[0, vocal_idx].numpy().T  # (samples, channels)
    
    out_path = OUT_DIR / f"{name}_vocals.wav"
    sf.write(str(out_path), vocals, sr)
    print(f"  Saved: {out_path}")

print("\nDone! All vocals extracted.")
