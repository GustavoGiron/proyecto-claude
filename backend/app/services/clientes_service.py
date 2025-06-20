# backend/app/services/clientes_service.py

from app.repositories.clientes_repo import ClienteRepo
from app.models.clientes_model import Cliente
from app.models.departamentos_model import Departamento
from sqlalchemy import func

class ClienteService:
    @staticmethod
    def list_all():
        return ClienteRepo.all()

    @staticmethod
    def get_by_id(id):
        return ClienteRepo.get(id)

    @staticmethod
    def get_by_codigo(codigo):
        return ClienteRepo.get_by_codigo(codigo)

    @staticmethod
    def create(data):
        # Quitamos claves que no deben venir del cliente
        data.pop('numero_cliente', None)
        data.pop('codigo_cliente', None)

        # 1) Generar numero_cliente global, si lo sigues usando:
        last = Cliente.query.order_by(Cliente.numero_cliente.desc()).first()
        next_num = last.numero_cliente + 1 if last else 1
        data['numero_cliente'] = next_num

        # 2) Obtener código del departamento
        dept = Departamento.query.get(data['departamento_id'])
        if not dept:
            raise ValueError(f"Departamento {data['departamento_id']} no encontrado")
        dept_code = dept.codigo.upper()

        # 3) Calcular siguiente correlativo para este departamento
        #    Buscamos todos los códigos que empiecen con dept_code
        rows = (
            Cliente.query
                   .with_entities(Cliente.codigo_cliente)
                   .filter(Cliente.codigo_cliente.startswith(dept_code))
                   .all()
        )
        # Extraemos la parte numérica y determinamos el máximo
        seq_nums = []
        for (code_str,) in rows:
            suffix = code_str[len(dept_code):]
            if suffix.isdigit():
                seq_nums.append(int(suffix))
        next_seq = max(seq_nums) + 1 if seq_nums else 1

        # 4) Formateamos el código de cliente: e.g. AL01, AL02, QZ01, GT01
        data['codigo_cliente'] = f"{dept_code}{next_seq:02d}"

        # 5) Creamos el cliente
        return ClienteRepo.add(data)

    @staticmethod
    def update(id, data):
        return ClienteRepo.update(id, data)

    @staticmethod
    def update_by_codigo(codigo, data):
        return ClienteRepo.update_by_codigo(codigo, data)

    @staticmethod
    def delete(id):
        return ClienteRepo.delete(id)

    @staticmethod
    def delete_by_codigo(codigo):
        return ClienteRepo.delete_by_codigo(codigo)