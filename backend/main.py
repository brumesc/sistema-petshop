from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class AgendamentoCreate(BaseModel):
    pet_id: int
    servico: str
    data_hora: datetime

class AgendamentoResponse(AgendamentoCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
from backend import models
from backend.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Pet Shop API", version="1.0.0")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- SCHEMAS PYDANTIC ---
class PetBase(BaseModel):
    nome: str
    especie: str
    raca: Optional[str] = None
    idade_anos: Optional[int] = None
    peso_kg: Optional[float] = None
    observacoes: Optional[str] = None

class PetCreate(PetBase):
    cliente_id: int

class PetResponse(PetBase):
    id: int
    cliente_id: int
    criado_em: datetime

    class Config:
        from_attributes = True

class ClienteBase(BaseModel):
    nome: str
    cpf: str
    telefone: str
    endereco: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    criado_em: datetime
    pets: List[PetResponse] = []

    class Config:
        from_attributes = True

# --- ROTAS CLIENTES ---
@app.post("/clientes/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.cpf == cliente.cpf).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    novo_cliente = models.Cliente(**cliente.model_dump())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@app.get("/clientes/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(models.Cliente).all()

# --- ROTAS PETS ---
@app.post("/pets/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def criar_pet(pet: PetCreate, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == pet.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    novo_pet = models.Pet(**pet.model_dump())
    db.add(novo_pet)
    db.commit()
    db.refresh(novo_pet)
    return novo_pet

@app.get("/pets/", response_model=List[PetResponse])
def listar_pets(db: Session = Depends(get_db)):
    return db.query(models.Pet).all()
@app.post("/agendamentos/", response_model=AgendamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_agendamento(agendamento: AgendamentoCreate, db: Session = Depends(get_db)):
    pet = db.query(models.Pet).filter(models.Pet.id == agendamento.pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    novo_agendamento = models.Agendamento(**agendamento.model_dump())
    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)
    return novo_agendamento

@app.get("/agendamentos/", response_model=List[AgendamentoResponse])
def listar_agendamentos(db: Session = Depends(get_db)):
    return db.query(models.Agendamento).all()