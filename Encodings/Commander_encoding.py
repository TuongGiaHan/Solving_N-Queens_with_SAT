
def add_amo(builder, var, group_size=3):
    m = len(var)

    if m <= 1:
        return

    if group_size < 2:
        raise ValueError()

    groups = [
        var[i:i + group_size]
        for i in range(0, m, group_size)
    ]

    commands = []

    for group in groups:
        com = builder.new_var()
        commands.append(com)

        for x in group:
            builder.add_clause([-x, com])
        builder.add_clause([-com] + group)

        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                builder.add_clause([-group[i], -group[j]])

    for i in range(len(commands)):
        for j in range(i + 1, len(commands)):
            builder.add_clause([
                -commands[i],
                -commands[j]
            ])
