import json


class Tabla:
    def __init__(self):
        self.data = {}
        self.crear_tabla()

    def crear_tabla(self):
        print('creating table')
        self.read_file()

    def read_file(self):
        file = open('tabla.json', mode = 'r')

        json_data = json.load(file)

        for json_object in json_data:

            if json_object['yname'] in self.data:
                interno = self.data[json_object['yname']]
                if not json_object['xtoken'] in interno:
                    interno[json_object['xtoken']] = json_object['produccion']
                    self.data[json_object['yname']] = interno
                else:
                    print('Error, interno ya existe')
                    return
            else:
                temp_interno = {json_object['xtoken']: json_object['produccion']}
                self.data[json_object['yname']] = temp_interno


        # print(self.data)

    def buscar_produccion(self, nt, t):
        if nt in self.data:
            interno = self.data[nt]
            if t in interno:
                return interno[t]

        return None

    def get_production_of(self, nt):
        if nt in self.data:
            interno = self.data[nt]
            return interno