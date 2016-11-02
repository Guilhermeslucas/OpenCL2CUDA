 __ void vadd(  float *a,   float *b,   float *c, const unsigned int n)
{
  //Get our global thread ID
  int id = blockIdx * blockDim + threadIdx;

  // Make sure we do not go out of bounds
  if (id < n) {
    c[id] = a[id] + b[id];
  }
}
