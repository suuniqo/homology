from filtered_simplicial_complex import FilteredSimplicialComplex

def main():
    sc = FilteredSimplicialComplex([])
    sc.insert([(0,1)], 1.0)
    sc.insert([(1,2), (2,3), (2,4)], 2.0)
    sc.insert([(3,4)], 3.0)
    sc.insert([(2,3,4)], 4.0)

    print(sc.face_set)

    print(sc.threshold((3,)))

    k1 = sc.filtration(1.0)
    k2 = sc.filtration(2.0)
    k3 = sc.filtration(3.0)
    k4 = sc.filtration(4.0)

    print(k1.face_set)
    print(k2.face_set)
    print(k3.face_set)
    print(k4.face_set)

    print(sc.filtration_order)

if __name__ == "__main__":
    main()
