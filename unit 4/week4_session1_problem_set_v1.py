"""UPI solutions for Week 4, Session 1, Problem Set Version 1."""


# 1. U: Each villager owns an initially empty furniture list.
# P: Store the three required arguments on the instance.
class Villager:
    def __init__(self, name, species, catchphrase):
        self.name = name
        self.species = species
        self.catchphrase = catchphrase
        self.furniture = []

    # 2. U: Only the five listed furniture names are valid.
    # P: Append the item only when it belongs to the allowed collection.
    def add_item(self, item_name):
        valid_items = {
            "acoustic guitar", "ironwood kitchenette", "rattan armchair",
            "kotatsu", "cacao tree",
        }
        if item_name in valid_items:
            self.furniture.append(item_name)


# Preserve the original constructor for Problems 1 and 2 before updating it.
BasicVillager = Villager


# 3 and 4 update the constructor with personality and an optional neighbor.
class Villager(BasicVillager):
    def __init__(self, name, species, personality, catchphrase, neighbor=None):
        super().__init__(name, species, catchphrase)
        self.personality = personality
        self.neighbor = neighbor


# 3. U: Return matching names, not the Villager objects.
# P: Visit each villager and append its name if the personality matches.
def of_personality_type(townies, personality_type):
    names = []
    for villager in townies:
        if villager.personality == personality_type:
            names.append(villager.name)
    return names


# 4. U: Messages can travel only along neighbor references.
# P: Follow neighbors, stopping at the target, None, or a repeated villager.
def message_received(start_villager, target_villager):
    visited = set()
    current = start_villager
    while current is not None and current not in visited:
        if current is target_villager:
            return True
        visited.add(current)
        current = current.neighbor
    return False


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def print_linked_list(head):
    current = head
    while current:
        print(current.value, end=" -> " if current.next else "\n")
        current = current.next


# 5. U: Connect the provided nodes in the specified order.
# P: Set each node's next pointer to the following node.
kk_slider = Node("K.K. Slider")
harriet = Node("Harriet")
saharah = Node("Saharah")
isabelle = Node("Isabelle")
kk_slider.next = harriet
harriet.next = saharah
saharah.next = isabelle


if __name__ == "__main__":
    apollo = BasicVillager("Apollo", "Eagle", "pah")
    assert (apollo.name, apollo.species, apollo.catchphrase, apollo.furniture) == (
        "Apollo", "Eagle", "pah", [],
    )
    alice = BasicVillager("Alice", "Koala", "guvnor")
    alice.add_item("acoustic guitar")
    alice.add_item("cacao tree")
    alice.add_item("nintendo switch")
    assert alice.furniture == ["acoustic guitar", "cacao tree"]
    assert apollo.furniture == []
    izzy = Villager("Isabelle", "Dog", "Normal", "what's up?")
    bob = Villager("Bob", "Cat", "Lazy", "pthhhpth")
    stitches = Villager("Stitches", "Cub", "Lazy", "stuffin'")
    assert of_personality_type([izzy, bob, stitches], "Lazy") == ["Bob", "Stitches"]
    assert of_personality_type([izzy, bob, stitches], "Cranky") == []
    tom = Villager("Tom Nook", "Raccoon", "Cranky", "yes, yes")
    kk = Villager("K.K. Slider", "Dog", "Lazy", "dig it")
    izzy.neighbor = tom
    tom.neighbor = kk
    assert message_received(izzy, kk) is True
    assert message_received(kk, izzy) is False
    kk.neighbor = tom
    assert message_received(kk, izzy) is False
    assert kk_slider.next is harriet
    assert harriet.next is saharah
    assert saharah.next is isabelle
    assert isabelle.next is None
    print_linked_list(kk_slider)
