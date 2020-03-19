/* Secure MPC Emulation Demo. (c) 2020 Swapnil Sayan Saha */

import shared3p;
import stdlib;
import shared3p_random;
import shared3p_sort;
import shared3p_statistics_summary;
import shared3p_statistics_outliers;
import shared3p_statistics_distribution;
import shared3p_statistics_regression;
import oblivious;
import shared3p_oblivious;
import aby;
import spdz_fresco;
domain pd_shared3p shared3p;
domain pd_spdz_fresco spdz_fresco;
domain pd_aby aby;

//secure user defined function to calculate vector sum
template<domain D : shared3p, type T>
D T[[1]] vecSum(D T[[1]] x, D T[[1]] y,D T[[1]] z){
    return sqrt((x*x)+(y*y)+(z*z));
}

//secure user defined functions for calculating filtered average of a vector
template<domain D, type T>
D T vecSum(D T [[1]] val, D T carry) {
    assert(size(val) > 0);

    uint n = size(val);
    if (n == 1) {
        return carry + val[0];
    }

    if (n % 2 == 0) {
        return vecSum(val[0:n/2] + val[n/2:n], carry);
    } else {
        return vecSum(val[0:n/2] + val[n/2:n-1], carry + val[n-1]);
    }
}

template<domain D, type T>
D T vecSum(D T [[1]] val) {
    assert(size(val) > 0);
    D T carry = 0;
    return vecSum(val, carry);
}

template<domain D, type T>
T vecAvg(D T [[1]] val, D T [[1]] mask) {
    assert(size(val) == size(mask));
    assert(size(val) > 0);

    uint n = size(val);
    if (n == 1) {
        return declassify(val[0] * mask[0]);
    }

    val = val * mask;
    D T sum = vecSum(val);
    D T count = vecSum(mask);

    return declassify(sum) / declassify(count);
}


void main(){
/*
PROTOCOL USED FOR MAXIMUM TESTS: SHARED 3P (secret shared data is collected on three aggregator nodes)
Secure against semi-honest adversaries
*/

/*three private datasets among collaborating hospitals*/

uint sizeA = 100;
uint sizeB = 50;
uint sizeC = 1000;
pd_shared3p float64[[1]] partyA(sizeA);
pd_shared3p float64[[1]] partyB(sizeB);
pd_shared3p float64[[1]] partyC(sizeC);
partyA[:] = {1.27, 2.776, 1.531, 4.321, 1.614, 7.316, 6.764, 6.873, 5.618, 5.465, 0.191, 4.344, 9.742, 1.056, 1.253, 1.341, 8.788, 6.377, 7.546, 5.265, 0.824, 1.898, 6.554, 4.696, 8.573, 4.842, 9.167, 2.573, 0.773, 3.821, 5.74, 0.927, 6.253, 2.909, 2.149, 2.655, 7.543, 1.755, 7.466, 1.781, 8.381, 5.868, 4.6, 4.603, 7.898, 7.048, 7.415, 8.83, 2.824, 4.482, 3.37, 7.443, 3.182, 3.893, 8.107, 7.716, 0.642, 6.797, 0.57, 0.246, 7.438, 4.188, 9.798, 6.035, 8.731, 3.603, 8.795, 2.546, 1.388, 8.801, 7.368, 8.01, 9.321, 0.581, 7.498, 3.039, 8.113, 8.154, 8.432, 5.458, 3.058, 0.978, 0.437, 8.395, 9.574, 6.588, 8.987, 1.666, 6.122, 6.336, 0.395, 5.467, 1.358, 5.895, 3.52, 4.789, 9.481, 8.713, 0.139, 2.146};
partyB[:] = {48.1, 34.569, 25.753, 41.607, 31.756, 16.272, 22.597, 42.035, 20.391, 40.216, 29.856, 13.278, 32.823, 21.228, 9.085, 9.919, 16.269, 3.597, 47.542, 2.909, 21.925, 42.34, 6.706, 23.875, 5.401, 42.756, 37.553, 15.379, 3.924, 25.325, 19.688, 20.706, 45.272, 44.03, 16.273, 45.757, 6.274, 2.891, 20.142, 17.518, 18.182, 7.458, 25.127, 21.99, 29.285, 47.505, 18.892, 21.716, 36.954, 7.159};
partyC[:] = {60.935, 16.219, -28.487, 25.895, 74.813, -70.579, -34.668, 26.211, -6.687, -37.361, 24.612, 6.511, 27.966, 34.579, 1.128, 73.705, 38.049, -76.67, 43.381, -63.707, 72.868, 75.982, -77.944, -15.901, -93.704, 58.962, -3.704, 30.448, 53.596, -99.16, 8.249, 66.046, 86.147, 50.72, -24.402, -89.99, 27.206, -3.908, -15.619, 90.026, 50.856, 1.354, -14.947, 18.393, 8.524, -46.324, 65.568, -57.904, -63.447, -46.325, 72.787, 62.611, -7.92, 98.812, -1.772, 72.906, -11.453, -50.807, -11.791, 2.001, -74.308, 72.001, -1.902, -19.977, 60.198, -34.384, -78.449, 61.194, 20.301, -89.123, -72.496, 97.49, -73.902, -27.264, -54.629, -8.545, -28.275, -16.51, -44.001, -57.94, -56.641, 82.143, -87.252, -76.955, -27.682, 20.555, 51.988, 31.879, 28.845, 26.398, -92.698, 56.06, -11.391, -69.22, 77.47, 19.094, -32.082, 75.193, 33.088, -52.734, 96.442, 66.228, -66.531, 66.596, 52.233, 62.858, -46.039, -1.057, -46.502, 86.886, -12.963, 18.002, 25.782, 89.534, -78.832, -4.54, -3.02, 63.874, 11.366, -77.587, 53.693, 69.89, 52.38, 77.019, 55.391, 31.708, 53.849, -66.145, 99.9, 4.921, -20.973, 25.297, -45.833, 38.705, -49.595, -66.267, 42.341, 24.743, 57.847, -17.891, -39.175, -87.765, -37.475, 22.068, 44.06, 21.354, 49.881, -72.732, -24.721, 14.159, -5.784, -47.744, -29.1, -46.902, 99.427, -96.831, -90.853, -53.102, 53.646, 70.433, -83.088, -0.374, -16.894, 42.789, -80.681, 79.944, -18.692, -57.08, -27.815, 23.419, -75.876, 40.311, 57.312, 28.011, -95.688, -85.843, 44.665, 98.218, -17.468, -8.001, 23.769, 15.043, 99.339, 84.34, 97.614, -75.895, 38.024, -29.92, -15.736, -80.324, 63.279, 75.917, -76.995, -33.967, 83.13, -21.485, -4.948, 29.701, -82.106, -67.728, -66.766, -91.463, -77.078, 85.258, 74.954, -42.831, -21.548, 19.859, -21.997, 95.936, -79.045, 22.053, -86.922, 88.504, 70.33, -64.218, 27.95, -13.217, -12.941, 6.343, -29.628, -9.787, -38.747, 43.896, -29.231, 62.554, 32.171, -99.373, 77.382, -68.807, 0.578, -67.705, -15.425, 12.593, 30.489, -76.704, -23.866, 42.551, 34.121, 19.006, 70.821, -28.426, -21.477, 15.115, 78.483, 45.285, 57.155, 91.573, -35.37, -62.436, -77.095, -1.081, -7.582, -74.904, 44.198, -59.09, -23.277, 27.876, 70.514, -26.398, -14.631, 66.341, -93.451, 80.52, 18, 92.286, 0.772, 46.866, 47.836, 64.432, -36.511, 72.162, 58.409, 99.864, 40.169, -62.283, 52.558, -7.669, 96.857, -20.623, 90.219, -98.654, 26.787, 20.497, 42.712, 46.018, 91.61, 49.438, -85.636, -34.945, -74.126, 25.809, 76.168, 23.744, -29.357, -61.81, -20.718, -6.853, -67.167, -17.077, 88.131, 97.743, 69.354, 91.129, -23.233, -64.136, 1.925, -26.173, -37.834, 65.087, 17.362, -37.965, -57.47, 42.686, 26.295, -78.5, -59.592, -95.513, -3.627, 73.966, -40.706, 37.475, -74.365, 63.447, -12.81, -90.084, -77.867, -78.056, -10.333, -65.135, -50.322, 65.583, 18.933, -93.702, -85.893, 80.031, 59.48, 86.199, 29.606, 97.197, -17.893, 71.503, -51.728, -75.848, 62.486, 76.962, 23.872, 93.349, 57.509, 60.569, 76.473, -39.702, -49.709, 36.556, 41.686, -24.765, 22.497, 13.576, 90.81, 98.051, 54.643, -54.481, 51.031, 79.923, -64.136, 69.637, 78.967, -48.654, -63.182, -30.177, -48.108, 82.534, -34.747, -74.769, 69.408, -22.978, 36.431, -4.241, 27.323, 20.075, 62.848, -33.48, -95.216, -80.837, -6.539, -40.487, -37.824, -88.214, 68.54, -27.279, 40.273, 48.131, -93.816, -17.643, -6.235, 31.557, 88.989, -9.961, -38.294, -26.767, 87.68, 92.79, -90.597, -79.677, -89.519, -18.169, 79.169, -68.346, 39.848, 70.236, -5.646, 99.69, 55.146, -33.324, -49.529, -83.012, 4.449, -18.511, 43.106, -53.16, -32.854, -60.017, -70.365, 12.108, -67.103, -83.19, -73.025, -85.082, -74.139, 1.33, -72.558, 39.857, -56.009, 57.363, -50.206, 53.79, 50.42, -11.429, -45.488, 50.168, 71.885, -92.137, 32.94, 34.792, 5.77, 21.62, 37.821, 37.106, -12.981, 20.308, -18.323, 55.452, 80.023, 95.923, 41.956, -54.173, -55.051, -14.428, -60.729, 79.598, -44.08, -60.873, -99.732, 93.301, 73.3, 21.557, 7.943, 18.887, 65.856, 45.078, -90.891, -30.625, -26.388, -60.168, 66.329, 10.675, 89.275, -76.463, -15.962, 0.655, 22.165, -30.581, -7.002, -25.405, -12.177, 11.512, 47.746, 59.96, -84.566, -40.72, -33.754, -85.796, -70.098, -86.582, 86.902, -19.016, 39.036, 84.68, -24.094, -99.888, -62.164, 95.747, 39.493, 82.898, -66.552, 81.981, -35.139, 64.207, 88.948, -90.897, -37.451, 9.19, 54.363, 37.218, 62.691, 51.689, 16.581, 16.48, -97.341, -2.655, -3.185, 38.061, -71.897, 96.315, 60.61, -78.612, -49.931, -93.991, -27.034, -6.624, -29.759, 35.204, -89.991, 7.675, 31.69, 36.511, 36.852, 77.625, -32.167, -67.843, 74.195, -68.35, -31.895, 30.889, 50.229, 57.672, 77.857, -54.617, -26.27, 41.889, -53.733, 53.798, 12.497, -37.445, -72.874, 25.029, 73.266, -80.713, 35.934, 86.66, -87.38, 61.102, 83.863, -86.328, -21.168, -14.552, 99.202, 67.722, -67.085, 89.386, 3.637, -70.925, -58.165, 43.658, -79.794, 99.487, -51.804, -62.606, -21.334, 0.464, 94.057, -91.567, 32.605, 78.49, -12.051, -41.196, -16.437, 72.617, 52.044, -86.273, 96.019, -18.249, 39.067, -81.083, 60.348, -54.76, -78.505, 86.207, -0.217, -58.035, -98.942, -21.368, -81.51, -47.735, 52.49, -60.91, -51.226, -97.083, 29.445, 14.625, -91.008, -74.337, 90.638, -25.986, 26.741, -22.296, 51.73, -51.2, 2.607, 59.199, 16.508, -59.327, -94.4, -70.484, -87.662, -27.377, 75.629, 62.498, 54.495, 66.946, 18.147, -19.005, -39.243, -8.126, 27.36, 57.547, -50.482, 92.301, -12.262, -46.461, 63.893, -58.803, 75.276, 58.86, 67.266, 81.647, 99.769, 86.01, 38.061, -57.449, -1.803, -19.7, -94.794, -83.173, 58.129, -9.059, 35.194, -16.006, -29.149, 43.261, -90.837, -47.028, -27.749, -57.723, 61.408, 74.124, -40.174, 3.145, 76.205, 68.333, -5.407, -33.629, -15.536, 21.238, -99.4, 39.776, -48.561, -51.248, 55.892, -31.905, 41.789, 5.481, 98.669, -25.346, -26.872, -58.057, -4.972, -33.743, -91.255, -50.337, -16.335, -51.156, -3.574, -60.483, -15.906, 57.712, -29.901, 51.697, -73.529, -94.717, 35.545, -56.542, -0.229, -11.221, -75.222, -34.697, -99.171, 94.819, 99.083, 88.785, 66.021, -92.462, 63.327, 56.624, -99.521, 21.324, 37.637, 31.429, -36.443, -43.218, 84.857, 59.567, -63.405, -86.358, 65.632, 35.065, 37.32, 99.491, 30.181, 52.934, 0.524, 15.236, -4.16, 61.202, 82.078, -32.721, 74.771, 12.637, 88.943, -36.494, 30.271, -15.51, 38.155, 46.505, 37.289, 71.45, -88.507, 64.502, 14.858, -22.399, -60.345, 41.192, -65.424, 7.719, -51.523, -26.569, 31.641, 0.442, -17.733, 84.454, -33.624, -65.838, 39.877, -13.196, 34.097, 31.655, 23.305, 88.009, 22.546, 72.449, -47.859, -47.674, 15.176, -19.258, 53.625, 41.573, -43.074, 8.507, 30.025, -5.881, 16.615, -92.935, 34.384, 96.588, 14.413, -26.413, 10.736, 38.068, -88.916, -96.006, 37.386, 39.961, -18.503, -36.015, 8.727, -10.653, -40.887, 23.474, 20.991, 39.867, -65.806, -75.365, 41.698, -83.501, 69.27, 39.954, 47.217, 94.814, 51.917, 5.429, -63.879, -99.991, 15.764, -86.47, -33.018, 11.88, -60.428, -56.235, -55.271, 55.541, -85.912, 17.075, -24.526, -0.387, 34.358, 96.579, -65.101, 19.274, -99.938, 52.062, -19.887, 23.912, -85.836, 24.774, 18.764, 10.538, -33.818, -82.662, 87.652, -48.072, 16.451, 78.096, 51.983, -89.548, -72.342, 77.332, 55.569, -97.34, -51.889, -7.449, -71.539, -61.245, -34.522, 15.365, 24.835, 58.011, 4.786, -31.508, 26.483, -14.481, -58.972, -96.718, 73.376, 18.47, 68.479, 82.407, 72.752, -53.759, 17.133, 20.262, -27.512, -38.92, -68.173, -34.261, 27.599, -37.829, 69.587, 62.923, 46.649, -44.897, -33.541, -51.493, -14.204, 58.137, 2.732, 90.837, 3.719, 0.904, 19.636, -29.36, -90.634, -14.797, 24.142, -20.559, -44.427, 48.656, 43.642, -73.048, 24.873, 91.053, -56.524, -73.86, 15.589, -78.006, 64.919, 37.622, 50.718, -97.226, -31.688, 16.477, 91.131, 7.634, 31.363, -85.904, -68.676, 64, 15.414, 32.262, -31.302, -39.481, -28.403, -6.2, 23.419, 48.832, -42.161, 80.559, -47.187, 9.799, -62.95, -63.816, -28.215, 60.656, 41.892, 45.069, -45.613, -53.113, -51.053, -96.865, 64.966, -56.811, -54.592, 41.071, 95.84, 77.542, -39.731, 55.29, -32.049, -48.643, -42.455, 27.612, -85.143, -22.4, 8.386, 74.589, -25.824, -44.937, -9.235, -13.669, -2.763, 59.62, 8.651, 78.011, 26.614, 26.065, -82.273, 85.061, 91.75, -69.565, 97.835, 94.565, -24.505, 2.294, 17.878, 17.455, -89.717, -75.681, 65.21, -83.07, -6.514, 93, -67.997, 16.758, -76.204, -40.065, 44.931, -60.912, -40.537, 55.998, 5.085, 65.069, 95.241, -9.052, -83.747, 46.042, 83.677, -58.364, -41.232, 49.23, -63.676, -53.306};

/*secure shuffle*/

shufpartyA = shuffle(partyA);
shufpartyB = shuffle(partyB);
shufpartyC = shuffle(partyC);
printVector(declassify(shufpartyA));
printVector(declassify(shufpartyA));
printVector(declassify(shufpartyA));


/*secure join and sort*/

//secure quicksort

pd_shared3p float64[[1]] secsortA = quicksort(partyA);
pd_shared3p float64[[1]] secsortB = quicksort(partyB);
pd_shared3p float64[[1]] secsortC = quicksort(partyC);
printVector(declassify(secsortA));
printVector(declassify(secsortB));
printVector(declassify(secsortC));



//secure join
pd_shared3p float64[[1]] sharedA = partyA[0:size(partyB)];
pd_shared3p float64[[1]] joinAB = cat(partyB,sharedA);

//secure union and intersection using oblivious functions
pd_shared3p float64[[1]] intersectAB(size(joinAB));
uint k = 0;
for(uint i = 0; i < size(sharedA); ++i){
   for(uint j = 0; j < size(partyB); ++j){
       pd_shared3p bool[[0]] truecond = true;
       pd_shared3p bool[[0]] falsecond = false;
       pd_shared3p bool[[0]] cond = choose(sharedA[i] == partyB[j],truecond,falsecond);
       if(declassify(cond)){
           intersectAB[k] = sharedA[i];
           k++;
       }
   }
}
intersectAB = intersectAB[0:k];

pd_shared3p float64[[1]] unionAB(size(joinAB));
uint f = 0;
k = 0;
for(uint i = 0; i <size(sharedA); ++i){
    unionAB[k] = sharedA[i];
    k++;
}
for(uint i = 0; i <size(partyB); ++i){
    f  = 0;
    for(uint j=0; j<size(sharedA); ++j){
        pd_shared3p bool[[0]] truecond = true;
        pd_shared3p bool[[0]] falsecond = false;
        pd_shared3p bool[[0]] cond = choose(partyB[i] == sharedA[j],truecond,falsecond);
        if(declassify(cond)) {
            f = 1;
        }
    }
    if(f == 0) {
    unionAB[k] = partyB[i];
    k++;
    }
}
unionAB = unionAB[0:k];
printVector(declassify(intersectAB));
printVector(declassify(unionAB));


/* secure feature extraction */

//for joint set unionAB
pd_shared3p bool[[1]] avVec(size(unionAB));
avVec = true;

pd_shared3p float64[[0]] mad = MAD(unionAB);
print(declassify(mad)); //MAD
pd_shared3p float64[[1]] fns = fiveNumberSummary(unionAB,avVec);
printVector(declassify(fns)); //min, lower_q, median, upper_q, maximum
pd_shared3p float64[[0]] avg = mean(unionAB);
print(declassify(avg)); //Mean
pd_shared3p float64[[0]] stddev = standardDev(unionAB);
print(declassify(stddev)); //Std_Dev
pd_shared3p float64[[0]] var = variance(unionAB);
print(declassify(var)); //Variance

//for vectorSum of part of A,B,C
pd_shared3p float64[[1]] sharedC = partyC[50:size(partyB)+50];
pd_shared3p float64[[1]] vecSumSharedABC = vecSum(sharedA, partyB, sharedC);

pd_shared3p bool[[1]] VSavVec(size(vecSumSharedABC));
VSavVec = true;

pd_shared3p float64[[0]] vecmad = MAD(vecSumSharedABC);
print(declassify(vecmad)); //MAD
pd_shared3p float64[[1]] vecfns = fiveNumberSummary(vecSumSharedABC,VSavVec);
printVector(declassify(vecfns)); //min, lower_q, median, upper_q, maximum
pd_shared3p float64[[0]] vecavg = mean(vecSumSharedABC);
print(declassify(vecavg)); //Mean
pd_shared3p float64[[0]] vecstddev = standardDev(vecSumSharedABC);
print(declassify(vecstddev)); //Std_Dev
pd_shared3p float64[[0]] vecvar = variance(vecSumSharedABC);
print(declassify(vecvar)); //Variance

//outlier detection using median absolute deviation
pd_shared3p bool[[1]] outliers = outlierDetectionMAD(unionAB, avVec, 4.0);
pd_shared3p float64[[1]] outFreeUnionAB(size(unionAB));
k = 0;
for(uint i = 0; i<size(unionAB); ++i){
    if(declassify(outliers[i]) == true){
        outFreeUnionAB[k] = unionAB[i];
        k++;
    }
}
outFreeUnionAB = outFreeUnionAB[0:k];
printVector(declassify(outFreeUnionAB));
print(size(outFreeUnionAB));

//outlier detection using quantiles
pd_shared3p bool[[1]] outliers_2 = outlierDetectionQuantiles(0.06, unionAB, avVec);
pd_shared3p float64[[1]] outFreeUnionAB_2(size(unionAB));
k = 0;
for(uint i = 0; i<size(unionAB); ++i){
    if(declassify(outliers_2[i]) == true){
        outFreeUnionAB_2[k] = unionAB[i];
        k++;
    }
}
outFreeUnionAB_2 = outFreeUnionAB_2[0:k];
printVector(declassify(outFreeUnionAB_2));
print(size(outFreeUnionAB_2));


/*secure machine learning*/

//simple linear regression
pd_shared3p float64[[1]] linreg = simpleLinearRegression(sharedA, partyB, VSavVec);
printVector(declassify(linreg));

/*other oblivious tasks*/

//update dataset obliviously
printVector(declassify(sharedC[0:3]));
pd_shared3p uint[[0]] index = 0;
pd_shared3p float64[[0]] newVal = -777.0;
sharedC = vectorUpdate(sharedC,index,newVal);
printVector(declassify(sharedC[0:3]));

/*testing other protocols - ABY and SPDZ-FRESCO*/
//the emulator does not have custom functions for working woth ABY or SPDZ-FRESCO yet.
//this is just for demo. I designed a filtered average using homomorphic operators which can be used.

uint [[1]] pubVal = {1, 2, 11, 0, 11, 0, 8, 3, 22, 13};
bool [[1]] pubMask = {true, false, true, false, true, false, true, false, true, false};

{ // pd_aby
    pd_aby uint64 [[1]] val = pubVal;
    pd_aby uint64 [[1]] mask = (uint) pubMask;
    uint average = vecAvg(val, mask);
    print(average);
}
{ // pd_shared3p
    pd_shared3p uint64 [[1]] val = pubVal;
    pd_shared3p uint64 [[1]] mask = (uint) pubMask;
    uint average = vecAvg(val, mask);
    print(average);
}
{ // pd_spdz_fresco
    pd_spdz_fresco uint64 [[1]] val = pubVal;
    pd_spdz_fresco uint64 [[1]] mask = (uint) pubMask;
    uint average = vecAvg(val, mask);
    print(average);
}

}



