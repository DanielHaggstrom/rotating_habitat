# rotating_habitat
Trajectories of objects within a rotating reference frame.

This is a simulation of an observer situated in a rotating space habitat like an O'Neill cylinder.
The observer watches a point-like object (`Ball`) releashed at some position with some speed, until it hits the side of the cylinder, or enough time passes.

There are two main methods to create an throw balls, `Cylinder.throw_still` and `Cylinderthrow_ball`.
- The first one is to be used for a cylinder that is still. The ball created can be in any location (specified as an array of coordinates [x, y] taking into account that tthe cylinder has a radius of one) and with any initial speed (again, in an array [v_x, v_y]).
- The second one is to be used for spinning cylinders. In this case, the initial position will always have a x coordinate of zero, and the y coordinate will be introduced as a fraction of the cylinder's radius, measured from the bottom and upwards. The speed is to be introduced in an array where the first element is the magnitude of the speed relative to the rotational speed at that height (measured by a rotating observer, when initialising the `Ball` object the inertia will be added) and the angle of the throw, measured from the bottom in the spinward direction.
