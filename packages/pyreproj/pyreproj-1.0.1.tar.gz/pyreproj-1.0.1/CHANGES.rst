1.0.1
~~~~~

https://gitlab.com/gf-bl/python-reprojector/milestones/1

- Set up deployment
- Lock version of pyproj<2.0.0

1.0.0
~~~~~

- Initial version
- Features:
    - define projections by projection object, proj4 definition or EPSG code
    - get projection by service (e.g. http://spatialreference.org/)
    - get a transformation function from source to target projection
    - transform coordinates as list or tuple or a shapely geometry directly
