# This file is part of quantumsim. (https://gitlab.com/quantumsim/quantumsim)
# (c) 2016 Brian Tarasinski
# Distributed under the GNU GPLv3. See LICENSE.txt or
# https://www.gnu.org/licenses/gpl.txt


def partial_greedy_toposort(partial_orders, targets=set()):
    """Given a list of partial orders ``[p1, p2, ...]`` of hashable items
    ``pi = [a_i0, a_i1, ...]``, representing the constraints

    .. math::

        a_{i0} < a_{i1} < ...

    construct a total ordering :math:`P: i_0 < i_1 < i_2 < ...`

    Some of the lists are denoted as target,
    and the ordering is chosen so that the number of overlaps between target
    lists is minimized, i.e. if ``p1`` and ``p2`` are targets, try to prevent

    .. math::

        a_{10} < a_{20} < a_{1n} < a_{2n}.

    This is done by a greedy algorithm.

    Parameters
    ----------
    partial_order: list
        List of lists of items, representing partial sequences
    targets: list
        List of indices into partial_order, signifying which lists are targets
    """

    targets = set(targets)

    # drop out empty lists
    partial_orders = [po for po in partial_orders if po]

    order_dicts = []
    for n, p in enumerate(partial_orders):
        order_dict = {i: j for i, j in zip(p[1:], p)}
        order_dicts.append(order_dict)

    trees = []
    for n, p in enumerate(partial_orders):
        tree = []
        to_do = [(None, p[-1])]
        while to_do:
            n, x = to_do.pop()
            tree.append((n, x))
            for n2, o2 in enumerate(order_dicts):
                x2 = o2.get(x)
                if x2 is not None:
                    to_do.append((n2, x2))

        lists_used = {n for n, x in tree if n in targets}
        trees.append((tree, lists_used))

    result = []
    all_used = set()
    while trees != []:
        trees.sort(key=lambda xy: len(all_used | xy[1]), reverse=True)
        smallest = trees.pop()
        all_used |= smallest[1]
        smallest = smallest[0]
        smallest.reverse()
        smallest = [x for n, x in smallest]

        new_trees = []
        for l, i in trees:
            l2 = [(n, x) for n, x in l if x not in smallest]
            new_trees.append((l2, i))

        trees = new_trees

        for s in smallest:
            if s not in result:
                result.append(s)

    return result
