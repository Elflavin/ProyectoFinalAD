from FirebaseConn import firebase_admin
from firebase_admin import db


ref = db.reference('empleados')
ref_d = db.reference('departamentos')


class Empleado:

    def __init__(self, nombre, appellido, dni, departamento):
        self.nombre = nombre
        self.apellido = appellido
        self.dni = dni
        self.departamento = departamento

    def __repr__(self):
        if self.departamento is None:
            return f"Nombre: {self.nombre, self.apellido} | DNI: {self.dni} | Departamento: 'sin asignar'"
        else:
            return f"Nombre: {self.nombre, self.apellido} | DNI: {self.dni} | Departamento: {self.departamento}"

    @classmethod
    def creEmp(cls, empleado):
        nuevo_empleado = cls(empleado)
        if cls.findRef(nuevo_empleado.dni) is None:
            nuevo_empleado_dict = {
                'nombre': nuevo_empleado.nombre,
                'apellido': nuevo_empleado.apellido,
                'dni': nuevo_empleado.dni,
                'departamento': nuevo_empleado.departamento
            }
            ref.child('empleados').push(nuevo_empleado_dict)
        else:
            return {'status': 'Error', 'message': 'El DNI ya esta en uso'}

    @classmethod
    def delEmp(cls, dni):
        key = cls.findRef(dni)
        ref.child('empleados').child(key).delete()

    @classmethod
    def updEmp(cls, nombre=None, apellido=None, dni=None, departamento=None):
        update_data = {}
        if nombre is not None:
            update_data['nombre'] = nombre
        if apellido is not None:
            update_data['apellido'] = apellido
        if dni is not None:
            update_data['dni'] = dni
        if departamento is not None:
            update_data['departamento'] = departamento
            updDepNEmp = True

        key = cls.findRef(dni)
        ref.child('empleados').child(key).update(update_data)
        if updDepNEmp:
            cls.findAndUpdRefDep(departamento)

    @classmethod
    def getEmp(cls, dni):
        key = cls.findRef(dni)
        emp_data = ref.child('empleados').child(key).get()
        if emp_data:
            return cls(
                nombre=emp_data.get('nombre'),
                apellido=emp_data.get('apellido'),
                dni=emp_data.get('dni'),
                departamento=emp_data.get('departamento')
            )
        else:
            return None

    @classmethod
    def findRef(cls, dni):
        empleados = cls.ref.get()
        for key, empleado in empleados.items():
            if 'dni' in empleado and empleado['dni'] == dni:
                return key
        return None

    @classmethod
    def findAndUpdRefDep(cls, nombre):
        departamentos = cls.ref_d.get()
        for key, departamento in departamentos.items():
            if 'nombre' in departamento and departamento['nombre'] == nombre:
                query = ref.order_by_child('departamento').equal_to(departamento)
                resultados = query.get()

                if resultados:
                    ref_d.child(nombre).update({'n_emp': len(resultados)})
        return None