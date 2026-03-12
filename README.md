## open-ghana-id

An API for running cheap, fast pre-verification checks on Ghanaian IDs before you spend money on full KYC providers. It helps you quickly reject obviously bad or unreadable IDs (bad scans, missing MRZ/QR, etc.) so you can optimize KYC spend.

### Features

- **Validate Personal TIN** via the public GRA endpoint 
- **Validate Ghana Card by card number** via the same endpoint
- **Extract MRZ data** from Ghana Card and Passport images
- **Image enhancement pipeline** to improve OCR/MRZ quality
- **Detect and parse QR** from Voters ID to structured data
- **Drivers license OCR** with a simple text serializer

### Endpoints

| Name                         | Method | Path                          | Content-Type        |
|------------------------------|--------|-------------------------------|---------------------|
| Health check                 | GET    | `/`                           | -                   |
| Validate passport            | POST   | `/validate-passport`          | `multipart/form-data` |
| Validate Ghana card image    | POST   | `/validate-ghana-card`        | `multipart/form-data` |
| Validate voters ID           | POST   | `/validate-voters-id`         | `multipart/form-data` |
| Validate Ghana card number   | POST   | `/validate-ghana-card-number` | `application/json`  |
| Validate personal TIN        | POST   | `/validate-tin`               | `application/json`  |
| Validate drivers license     | POST   | `/validate-drivers-license`   | `multipart/form-data` |

### Quick start (UV)

```bash
uv sync
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000/docs`.

### Quick start (Docker)

```bash
docker compose up --build
```

Then open `http://localhost:8000/docs`.

### Legacy demo & docs (slow)

From the original closed-source service (may be slow or unavailable):

- Legacy demo API (Render): `https://apex-g3ka.onrender.com`
- Legacy Postman docs: `https://documenter.getpostman.com/view/8806007/2s8Z72WCHv`

These are kept for historical reference only and are **not** maintained.

### Tests

Minimal tests live under `tests/`:

- Core behaviour (health, JSON routes)
- GRA routes using mocks (no real HTTP calls)
- Optional image route checks that reuse legacy samples from `oval-id-service/samples/` if you have them locally

Run them with:

```bash
make test
```

### Future work

- More robust data extraction for drivers' licenses (move away from brittle, line-based OCR parsing to a structured model or template-based approach).
- Optional caching for GRA responses and/or expensive image-processing steps to reduce latency and external calls.

### Contributing

- Keep the API surface small and focused.
- Prefer clear, typed Python over comments.
- Do not commit any real personal data or secrets.

Issues and small PRs are welcome. This project is intentionally lightweight so it is easy to understand and extend.

### Acknowledgements

Thanks to [@saviour123](https://github.com/saviour123) and [@benacq](https://github.com/benacq) for their work on the original closed-source ID service that inspired this project.

### Disclaimer

This project is for educational and research use only. You are solely responsible for how you use it, including any interaction with government systems or personal data. I accept no liability for misuse.

