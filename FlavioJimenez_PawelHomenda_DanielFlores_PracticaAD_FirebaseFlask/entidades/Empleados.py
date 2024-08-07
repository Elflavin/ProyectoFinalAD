from entidades.Departamentos import Departamento
from fireb_init import init
from firebase_admin import db

try:
    init()
except ValueError:
    print("Base de datos ya definido.")



class Empleado:
    ref = db.reference('empleados')
    ref_d = db.reference('departamentos')

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
        nuevo_empleado = cls(empleado.nombre,empleado.apellido,empleado.dni,empleado.departamento)
        if cls.findRef(nuevo_empleado.dni) is None:
            nuevo_empleado_dict = {
                'nombre': nuevo_empleado.nombre,
                'apellido': nuevo_empleado.apellido,
                'dni': nuevo_empleado.dni,
                'departamento': nuevo_empleado.departamento
            }
            cls.ref.child('empleados').push(nuevo_empleado_dict)
        else:
            return {'status': 'Error', 'message': 'El DNI ya esta en uso'}

    @classmethod
    def getAllEmp(cls):
        tempRef = db.reference("empleados/empleados")

        return tempRef.get()

    @classmethod
    def delEmp(cls, dni):
        key = cls.findRef(dni)
        cls.ref.child('empleados').child(key).delete()

    @classmethod
    def updEmp(cls, empleado=None, obj=None):
        update_data = {}
        if empleado.nombre is not None:
            update_data['nombre'] = empleado.nombre
        if empleado.apellido is not None:
            update_data['apellido'] = empleado.apellido
        if empleado.dni is not None:
            update_data['dni'] = empleado.dni
        if empleado.departamento is not None:
            update_data['departamento'] = empleado.departamento
            updDepNEmp = True

        key = cls.findRef(obj)
        cls.ref.child('empleados').child(key).update(update_data)
        if updDepNEmp:
            cls.findAndUpdRefDep(empleado.departamento)

    @classmethod
    def getEmp(cls, dni):
        key = cls.findRef(dni)
        emp_data = cls.ref.child('empleados').child(key).get()
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
        if empleados is not None:
            for key, empleado in empleados['empleados'].items():
                if 'dni' in empleado and empleado['dni'] == dni:
                    return key
        return None

    @classmethod
    def findAndUpdRefDep(cls, dni, nombre):
        departamentos = cls.ref_d.get()
        empleados = cls.ref.get()
        for key, empleado in empleados['empleados'].items(): # Actualizar antiguo departamento
            if 'dni' in empleado and empleado['dni'] == dni and 'departamento' in empleado and empleado['departamento'] != nombre:
                for key, departamento in departamentos['departamentos']:
                    if 'nombre' in departamento and departamento['nombre'] == nombre and 'n_emp' in departamento:
                        query = cls.ref.order_by_child('departamento').equal_to(departamento['nombre'])
                        resultados = query.get()

                        if resultados:
                            cls.ref_d.child(Departamento.findRef(departamento['nombre'])).update({'n_emp': len(resultados)})

        for key, departamento in departamentos['departamentos'].items(): # Actualizar nuevo departamento
            if 'nombre' in departamento and departamento['nombre'] == nombre:
                query = cls.ref.order_by_child('departamento').equal_to(departamento['nombre'])
                resultados = query.get()

                if resultados:
                    cls.ref_d.child(Departamento.findRef(nombre)).update({'n_emp': len(resultados)})
        return None