# Tracked Files in the Carbon Intelligence Assistant Repository

## Frontend ( `frontend/` )

| Path | Size (bytes) | Reason it’s tracked |
|------|--------------|----------------------|
| `frontend/README.md` | 1157 | Not matched by any ignore pattern |
| `frontend/.gitignore` | 253 | The file itself is always tracked |
| `frontend/eslint.config.js` | 758 | No ignore rule for `*.js` |
| `frontend/index.html` | 357 | Not ignored |
| `frontend/package-lock.json` | 152762 | Not ignored |
| `frontend/package.json` | 775 | Not ignored |
| `frontend/postcss.config.js` | 80 | Not ignored |
| `frontend/tailwind.config.js` | 439 | Not ignored |
| `frontend/vite.config.js` | 161 | Not ignored |
| `frontend/public/` (contains `index.html` etc.) | – | Directory not ignored |
| `frontend/src/App.css` | 606 | Not ignored |
| `frontend/src/App.jsx` | 709 | Not ignored |
| `frontend/src/index.css` | 336 | Not ignored |
| `frontend/src/main.jsx` | 229 | Not ignored |
| `frontend/src/pages/Home.jsx` | 1551 | Not ignored |
| `frontend/src/pages/Prediction.jsx` | 3350 | Not ignored |
| `frontend/src/pages/Recommendations.jsx` | 3206 | Not ignored |
| `frontend/src/pages/Report.jsx` | 2214 | Not ignored |
| `frontend/src/pages/Upload.jsx` | 2950 | Not ignored |
| `frontend/src/assets/` (any assets you added) | – | `assets/` folder is not ignored |

*The `node_modules/`, `dist/`, and `frontend/.parcel-cache/` directories are **ignored** by the `.gitignore`.*

## Backend ( `backend/` )

| Path | Size (bytes) | Reason it’s tracked |
|------|--------------|----------------------|
| `backend/.env` | 56 | Listed as project‑specific (currently tracked) |
| `backend/AGENTIC_ARCHITECTURE.md` | 3629 | Not ignored |
| `backend/Dockerfile` | 678 | Not ignored |
| `backend/main.py` | 7998 | Not ignored |
| `backend/requirements.txt` | 130 | Not ignored |
| `backend/models/` (all files) | – | No ignore rule for `models/` |
| `backend/services/` (all files) | – | No ignore rule for `services/` |
| `backend/agents/data_agent.py` | 2742 | Not ignored |
| `backend/agents/loop_agent.py` | 1588 | Not ignored |
| `backend/agents/optimization_agent.py` | 4112 | Not ignored |
| `backend/agents/prediction_agent.py` | 3853 | Not ignored |
| `backend/agents/__init__.py` | – | Not ignored |
| `backend/__pycache__/` (compiled byte‑code) | – | No ignore rule for `__pycache__/` |
| `backend/venv/` (virtual env) | – | Ignored by `.gitignore` (virtual‑env pattern) |

*If you prefer the `.env` file to stay private, add `backend/.env` to `.gitignore` and run `git rm --cached backend/.env`.*
