from fireb_init import init
from firebase_admin import db

try:
    init()
except ValueError:
    print("Base de datos ya definido.")



class Departamento:

    ref = db.reference('departamentos')

    def __init__(self, nombre, descr, lider, n_emp):
        self.nombre = nombre
        self.descr = descr
        self.lider = lider
        self.n_emp = n_emp

    def __repr__(self):
        if self.lider is None:
            return (f"Nombre: {self.nombre} | Descripcion: {self.descr} | Lider: 'sin asignar' | "
                    f"NºEmpleados: {self.n_emp}")
        else:
            return (f"Nombre: {self.nombre} | Descripcion: {self.descr} | Lider: {self.lider} | "
                    f"NºEmpleados: {self.n_emp}")

    @classmethod
    def creDep(cls, nombre, descr, lider, n_emp):
        nuevo_departamento = cls(nombre, descr, lider, n_emp)
        if cls.findRef(nuevo_departamento.nombre) is None:
            nuevo_departamento_dict = {
                'nombre': nuevo_departamento.nombre,
                'descr': nuevo_departamento.descr,
                'lider': nuevo_departamento.lider,
                'n_emp': nuevo_departamento.n_emp
            }
            cls.ref.child('departamentos').push(nuevo_departamento_dict)
        else:
            return {'status': 'Error', 'message': 'El nombre ya esta en uso'}


    @classmethod
    def delDep(cls, dep_id):
        cls.ref.child('departamentos').child(dep_id).delete()

    @classmethod
    def updDep(cls, departamento=None, obj=None):
        update_data = {}
        if departamento.nombre is not None:
            update_data['nombre'] = departamento.nombre
        if departamento.descr is not None:
            update_data['descr'] = departamento.descr
        if departamento.lider is not None:
            update_data['lider'] = departamento.lider
        if departamento.n_emp is not None:
            update_data['n_emp'] = departamento.n_emp

        key = cls.findRef(obj)
        cls.ref.child('departamentos').child(key).update(update_data)

    @classmethod
    def getDep(cls, dep_id):
        key = cls.findRef(dep_id)
        dep_data = cls.ref.child('departamentos').child(key).get()
        if dep_data:
            return cls(
                nombre=dep_data.get('nombre'),
                descr=dep_data.get('descr'),
                lider=dep_data.get('lider'),
                n_emp=dep_data.get('n_emp')
            )
        else:
            return None

    @classmethod
    def findRef(cls, nombre):
        departamentos = cls.ref.get()
        if departamentos is not None:
            for key, departamento in departamentos.items():
                if 'nombre' in departamento and departamento['nombre'] == nombre:
                    return key
        return None