from abc import ABC, abstractmethod
from typing import List
import copy

class Printable(ABC):
    """Base abstract class for printable objects."""
    
    def print_me(self, output, prefix="", is_final=False):
        """Display hierarchy structure"""
        pass
        
    @abstractmethod
    def clone(self):
        """Create deep copy"""
        pass

class BasicCollection(Printable):
    """Collection of items base"""
    def __init__(self):
        self.elements = []
    
    def add(self, item):
        self.elements.append(item)
        return self
    
    def find(self, target_name):
        return next((x for x in self.elements 
                   if isinstance(x, Computer) and x.name == target_name), None)
    
    def clone(self):
        return copy.deepcopy(self)

class Component(Printable):
    """Hardware component base"""
    def __init__(self, value=0):
        self.value = value
        
    def print_me(self, output, prefix="", is_final=False):
        symbol = '\\-' if is_final else '+-'
        output.append(f"{prefix}{symbol}{self.__class__.__name__}")
    
    def clone(self):
        return copy.deepcopy(self)

class Address(Printable):
    """Network endpoint"""
    def __init__(self, ip):
        self.ip = ip
    
    def print_me(self, output, prefix="", is_final=False):
        output.append(f"{prefix}{'+-'}{self.ip}")
    
    def clone(self):
        return copy.deepcopy(self)

class Computer(BasicCollection, Component):
    """Computer system"""
    def __init__(self, name):
        BasicCollection.__init__(self)
        Component.__init__(self)
        self.name = name
        self.network_points = []
    
    def add_address(self, ip):
        self.network_points.append(Address(ip))
        return self
    
    def add_component(self, part):
        self.add(part)
        return self
    
    def print_me(self, output, prefix="", is_final=False):
        marker = '\\-' if is_final else '+-'
        output.append(f"{prefix}{marker}Host: {self.name}")
        
        for i, point in enumerate(self.network_points):
            point.print_me(output, prefix + ("| " if not is_final else "  "), 
                         i == len(self.network_points) - 1)

        for i, part in enumerate(self.elements):
            part.print_me(output, prefix + ("| " if not is_final else "  "), 
                         i == len(self.elements) - 1)
    
    def clone(self):
        return copy.deepcopy(self)

class Network(Printable):
    """Computer network"""
    def __init__(self, name):
        self.name = name
        self.nodes = []
    
    def add_computer(self, node):
        self.nodes.append(node)
        return self
    
    def find_computer(self, node_name):
        return next((n for n in self.nodes if n.name == node_name), None)
    
    def print_me(self, output, prefix="", is_final=False):
        output.append(f"Network: {self.name}")
        for i, node in enumerate(self.nodes):
            node.print_me(output, prefix, i == len(self.nodes) - 1)
    
    def __str__(self):
        result = []
        self.print_me(result)
        return "\n".join(result)
    
    def clone(self):
        return copy.deepcopy(self)

class Disk(Component):
    """Storage device"""
    SSD, HDD = 0, 1
    
    def __init__(self, kind, capacity):
        super().__init__()
        self.kind = kind
        self.capacity = capacity
        self.sections = []
    
    def add_partition(self, size, label):
        self.sections.append((size, label))
        return self
    
    def print_me(self, output, prefix="", is_final=False):
        kind_str = 'SSD' if self.kind == Disk.SSD else 'HDD'
        symbol = '\\-' if is_final else '+-'
        output.append(f"{prefix}{symbol}{kind_str}, {self.capacity} GiB")
        
        for i, (size, name) in enumerate(self.sections):
            part_mark = '\\-' if i == len(self.sections) - 1 else '+-'
            output.append(f"{prefix}  {part_mark}[{i}]: {size} GiB, {name}")

class CPU(Component):
    """Processor unit"""
    def __init__(self, core_count, speed):
        super().__init__()
        self.cores = core_count
        self.speed = speed
    
    def print_me(self, output, prefix="", is_final=False):
        mark = '\\-' if is_final else '+-'
        output.append(f"{prefix}{mark}CPU, {self.cores} cores @ {self.speed}MHz")

class Memory(Component):
    """RAM module"""
    def __init__(self, capacity):
        super().__init__()
        self.capacity = capacity
    
    def print_me(self, output, prefix="", is_final=False):
        symbol = '\\-' if is_final else '+-'
        output.append(f"{prefix}{symbol}Memory, {self.capacity} MiB")

def execute_demo():
    """Demonstration function"""
    net = Network("University NET")
    
    net.add_computer(
        Computer("node1.uni.edu")
        .add_address("192.168.1.1")
        .add_component(CPU(4, 2500))
        .add_component(Memory(16000))
    ).add_computer(
        Computer("node2.uni.edu")
        .add_address("10.0.0.1")
        .add_component(CPU(8, 3200))
        .add_component(
            Disk(Disk.HDD, 2000)
            .add_partition(500, "system")
            .add_partition(1500, "storage")
        )
    )
    
    print("=== Network structure ===")
    print(net)
    
    expected = """Network: University NET
+-Host: node1.uni.edu
| +-192.168.1.1
| +-CPU, 4 cores @ 2500MHz
| \-Memory, 16000 MiB
\-Host: node2.uni.edu
  +-10.0.0.1
  +-CPU, 8 cores @ 3200MHz
  \-HDD, 2000 GiB
    +-[0]: 500 GiB, system
    \-[1]: 1500 GiB, storage"""
    
    assert str(net) == expected, "Output mismatch"
    print("✓ Format test passed")

if __name__ == "__main__":
    execute_demo()