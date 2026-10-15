from filtered_simplicial_complex import FilteredSimplicialComplex
from filtrations.alpha import alpha_filtration

from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import matplotlib.colors

# TODO: Plot the simpleces more efficiently
def alpha_test():
    LIMITE_K = 1
    PASO = 0.05

    points = [(0.38021546727456423, 0.46419202339598786), (0.7951628297672293, 0.49263630135869474), 
              (0.566623772375203, 0.038325621649018426), (0.3369306814864865, 0.7103735061134965), 
              (0.08272837815822842, 0.2263273314352896), (0.5180166301873989, 0.6271769943824689), 
              (0.33691411899985035, 0.8402045183219995), (0.33244488399729255, 0.4524636520475205), 
              (0.11778991601260325, 0.6657734204021165), (0.9384303415747769, 0.2313873874340855)]

    vor = Voronoi(points)
    fig = voronoi_plot_2d(vor,show_vertices=False, line_width=2, line_colors='red')
    plt.plot([points[i][0] for i in range(len(points))], 
             [points[i][1] for i in range(len(points))],
             'ko')

    alpha = alpha_filtration(points)

    print(alpha.filtration_order)
    print(alpha.treshold_values())

    for k in alpha.treshold_values():
        current = alpha.filtration(k)

        print(f"k={k}")
        plot_simplicials(points, current)

    # last_simplicial_no = 0
    # k = 0
    # while k < LIMITE_K:
    #     current = alpha.filtration(k)

    #     if len(current.face_set) == last_simplicial_no:
    #         k += PASO
    #         continue

    #     last_simplicial_no = len(current.face_set)

    #     print(f"k={k}")
    #     plot_simplicials(points, current)
        
    #     k += PASO

def plot_simplicials(points, current):
    color = matplotlib.colors.ListedColormap("limegreen")
    print(f"Number of simplicials: {len(current.face_set)}")

    for simplicial in current.face_set:
        if len(simplicial) == 1:
            plt.plot(points[simplicial[0]][0], points[simplicial[0]][1], 'ko')
        if len(simplicial) == 2:
            plt.plot([points[simplicial[0]][0], points[simplicial[1]][0]],
                         [points[simplicial[0]][1], points[simplicial[1]][1]],
                         color='k', lw=2)
        if len(simplicial) == 3:
            plt.tripcolor([points[simplicial[i]][0] for i in range(3)],
                              [points[simplicial[i]][1] for i in range(3)],
                              [simplicial[i] for i in range(3)],
                            #   [1, 1, 1],
                              edgecolor='k', lw=2,
                              cmap=color)
    plt.show()

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
    # main()
    alpha_test()
