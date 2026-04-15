from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import tempfile
from secrets import compare_digest

from ai_engine.role_predictor import role_predictor

router = APIRouter(prefix="/admin", tags=["admin"])
security = HTTPBasic()


def check_admin(creds: HTTPBasicCredentials = Depends(security)):
    admin_user = os.getenv('ADMIN_USER', 'admin')
    admin_pass = os.getenv('ADMIN_PASSWORD', 'admin')
    if not (compare_digest(creds.username, admin_user) and compare_digest(creds.password, admin_pass)):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return creds.username


@router.post("/role-predictor/retrain")
async def retrain_role_predictor(file: UploadFile | None = File(None), _=Depends(check_admin)):
    """Retrain the role predictor from an uploaded CSV (or bundled CSV if none).

    CSV should have columns like `text` and `role`.
    """
    csv_path = 'data/training_dataset.csv'
    if file:
        # save uploaded file temporarily
        suffix = os.path.splitext(file.filename)[1] or '.csv'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir='data') as tmp:
            content = await file.read()
            tmp.write(content)
            csv_path = tmp.name

    ok = role_predictor.train_from_csv(csv_path)
    if not ok:
        raise HTTPException(status_code=400, detail='Training failed or CSV invalid')

    saved = role_predictor.save_model()
    return {"status": "ok", "trained": role_predictor.trained, "saved": bool(saved)}


@router.get('/role-predictor/status')
def role_model_status(_=Depends(check_admin)):
    return {"trained": role_predictor.trained}
