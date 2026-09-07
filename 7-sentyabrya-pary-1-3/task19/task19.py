class CPU:
    def __init__(self, name, fr):
        self.name = name
        self.fr = fr


class Memory:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume


class MotherBoard:
    total_mem_slots = 4
    
    def __init__(self, name, cpu, *mem_slots):
        self.name = name
        self.cpu = cpu
        self.mem_slots = list(mem_slots)[:self.total_mem_slots]
    
    def get_config(self):
        config = []
        config.append(f'Материнская плата: {self.name}')
        config.append(f'Центральный процессор: {self.cpu.name}, {self.cpu.fr}')
        config.append(f'Слотов памяти: {self.total_mem_slots}')
        
        memory_list = []
        for mem in self.mem_slots:
            memory_list.append(f'{mem.name} - {mem.volume}')
        config.append(f'Память: {"; ".join(memory_list)}')
        
        return config


cpu = CPU('Ryzen 5 5600OEM', 3600)
mem1 = Memory('ADATA XPG', 8)
mem2 = Memory('ADATA XPG', 8)

mb = MotherBoard('GIGABYTE AORUS ELITE', cpu, mem1, mem2)