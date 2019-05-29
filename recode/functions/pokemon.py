def make_moveset(pokemon):
    pass
    # logic for learning moves:
    # if there are any free slots for learning, simply insert new move into slot.
    # Gather a list of possible moves that can be learned considering this pokemon's level.
    # There are only three types of move damage classes. Status, physical, and special. 
    # Prioritize learning moves that are physical/special for now. 
    # Forget moves that are status. 
    # If there are no moves that are status, prioritize same type + high damage. 
    # Same type is always given priority.
    # Primary type given priority over secondary type.
    # If type is not a concern, power level is the concern. 