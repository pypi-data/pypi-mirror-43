% add current folder to path
if count(py.sys.path,'') == 0  
    insert(py.sys.path,int32(0),'');
end

% import Compadre Toolkit
py.importlib.import_module('GMLS_Module');

% initialize Kokkos
py.GMLS_Module.initializeKokkos();

% set the polynomial order for the basis and the curvature polynomial order
% (if on a manifold)
poly_order = py.int(2);
curvature_poly_order = py.int(2);

dense_solver_type = py.str("QR");

% spatial dimension for polynomial reconstruction
spatial_dimensions = py.int(1);

% initialize and instance of the GMLS class in Compadre Toolkit
my_gmls = py.GMLS_Module.GMLS_Python(poly_order, dense_solver_type, curvature_poly_order, spatial_dimensions);

% set the weighting order
regular_weight = py.int(12);
my_gmls.setWeightingOrder(regular_weight);

% import the py_search module which uses kdtree in scipy
py_search = py.importlib.import_module('py_search');

% generate some 1d source points and a single target site
x=-10:.001:10;
x=[x' zeros(length(x),2)];
y=0;
y=[y' zeros(length(y),2)];
np_x = py_search.np.array(x);
np_y = py_search.np.array(y);
y_list_size = py.list([size(y,1),3]);
np_y = py_search.np.resize(np_y, y_list_size);

% manually calculated neighbor list
% neighbor_lists = [length(9990:1:10010) 9990:1:10010];
% neighbor_list_size = py.list([1, length(neighbor_lists)]);
% np_neighbor_lists = py_search.np.array(neighbor_lists);
% np_neighbor_lists = py_search.np.resize(np_neighbor_lists, neighbor_list_size);
% epsilons = [.15];
% np_epsilons = py_search.np.array(epsilons);
% epsilons_list_size = py.list([size(np_epsilons,2),1]);
% np_epsilons = py_search.np.resize(np_epsilons, epsilons_list_size);

% returns a dictionary with epsilons and with neighbor_lists
d = py_search.get_neighborlist(np_x,np_y,poly_order,spatial_dimensions);

my_gmls.setSourceSites(np_x);
my_gmls.setTargetSites(np_y);
my_gmls.setWindowSizes(d{'epsilons'});
my_gmls.setNeighbors(d{'neighbor_lists'});

% generates stencil
my_gmls.generatePointEvaluationStencil();

% apply stencil to sample data for all targets
data_vector = ones(size(x,1),1);
np_data_vector = py_search.np.array(data_vector);
computed_answer = my_gmls.applyStencil(np_data_vector)

% finalize kokkos
py.GMLS_Module.finalizeKokkos();


% if needed, py.reload(py_search);