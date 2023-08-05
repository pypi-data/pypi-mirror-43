#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/uint8.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/bool.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/uint8.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/include/__builtin__/None.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/idiv.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/__builtin__/None.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/idiv.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_operators2d
{
  struct __transonic__
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct compute_increments_dim1
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef pythonic::types::contiguous_slice __type1;
      typedef decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type1>())) __type2;
      typedef typename pythonic::returnable<decltype((std::declval<__type2>() - std::declval<__type2>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& var, argument_type1&& irx) const
    ;
  }  ;
  struct invlaplacian_fft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename pythonic::assignable<decltype((pythonic::operator_::div(std::declval<__type0>(), std::declval<__type1>())))>::type __type2;
      typedef long __type3;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type3>(), std::declval<__type3>())) __type4;
      typedef indexable<__type4> __type5;
      typedef typename __combined<__type2,__type5>::type __type6;
      typedef double __type7;
      typedef container<typename std::remove_reference<__type7>::type> __type8;
      typedef typename __combined<__type6,__type8>::type __type9;
      typedef typename __combined<__type9,__type5>::type __type10;
      typedef typename pythonic::returnable<typename __combined<__type10,__type8>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& a_fft, argument_type1&& Kn_not0, argument_type2&& rank) const
    ;
  }  ;
  struct laplacian_fft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename pythonic::returnable<decltype((pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type1>())))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& a_fft, argument_type1&& Kn) const
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral2D__dealiasing_setofvar
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type2;
      typedef decltype(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type3;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type3>::type>::type __type4;
      typedef typename pythonic::lazy<__type4>::type __type5;
      typedef decltype(std::declval<__type1>()(std::declval<__type5>())) __type6;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type6>::type::iterator>::value_type>::type __type7;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type __type8;
      typedef typename pythonic::lazy<__type8>::type __type9;
      typedef decltype(std::declval<__type1>()(std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type3>::type>::type __type12;
      typedef typename pythonic::lazy<__type12>::type __type13;
      typedef decltype(std::declval<__type1>()(std::declval<__type13>())) __type14;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type11>(), std::declval<__type15>())) __type16;
      typedef __type0 __ptype0;
      typedef __type16 __ptype1;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& self__has_to_dealiase, argument_type1&& self_where_dealiased, argument_type2&& sov) const
    ;
  }  ;
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.1.13"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 >
  typename compute_increments_dim1::type<argument_type0, argument_type1>::result_type compute_increments_dim1::operator()(argument_type0&& var, argument_type1&& irx) const
  {
    typename pythonic::assignable<decltype(std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, var)))>::type n1 = std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, var));
    ;
    ;
    return (var(pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None),pythonic::types::contiguous_slice(irx,n1)) - var(pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None),pythonic::types::contiguous_slice(0L,(n1 - irx))));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename invlaplacian_fft::type<argument_type0, argument_type1, argument_type2>::result_type invlaplacian_fft::operator()(argument_type0&& a_fft, argument_type1&& Kn_not0, argument_type2&& rank) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
    typedef typename pythonic::assignable<decltype((pythonic::operator_::div(std::declval<__type0>(), std::declval<__type1>())))>::type __type2;
    typedef long __type3;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type3>(), std::declval<__type3>())) __type4;
    typedef indexable<__type4> __type5;
    typedef typename __combined<__type2,__type5>::type __type6;
    typedef double __type7;
    typedef container<typename std::remove_reference<__type7>::type> __type8;
    typedef typename __combined<__type6,__type8>::type __type9;
    typename pythonic::assignable<typename __combined<__type9,__type5>::type>::type invlap_afft = (pythonic::operator_::div(a_fft, Kn_not0));
    if ((pythonic::operator_::eq(rank, 0L)))
    {
      invlap_afft.fast(pythonic::types::make_tuple(0L, 0L)) = 0.0;
    }
    return invlap_afft;
  }
  template <typename argument_type0 , typename argument_type1 >
  typename laplacian_fft::type<argument_type0, argument_type1>::result_type laplacian_fft::operator()(argument_type0&& a_fft, argument_type1&& Kn) const
  {
    return (pythonic::operator_::mul(a_fft, Kn));
  }
  typename __code_new_method__OperatorsPseudoSpectral2D__dealiasing_setofvar::type::result_type __code_new_method__OperatorsPseudoSpectral2D__dealiasing_setofvar::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral2D__dealiasing_setofvar::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, sov):\n"
"    return pythran_func(self._has_to_dealiase, self.where_dealiased, sov)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename __for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar::type<argument_type0, argument_type1, argument_type2>::result_type __for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar::operator()(argument_type0&& self__has_to_dealiase, argument_type1&& self_where_dealiased, argument_type2&& sov) const
  {
    if (self__has_to_dealiase)
    {
      typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type nk = std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov));
      typename pythonic::lazy<decltype(std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type n0 = std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov));
      typename pythonic::lazy<decltype(std::get<2>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type n1 = std::get<2>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov));
      {
        long  __target139984242699344 = n0;
        for (long  i0=0L; i0 < __target139984242699344; i0 += 1L)
        {
          {
            long  __target139984243175720 = n1;
            for (long  i1=0L; i1 < __target139984243175720; i1 += 1L)
            {
              if (self_where_dealiased.fast(pythonic::types::make_tuple(i0, i1)))
              {
                {
                  long  __target139984243176896 = nk;
                  for (long  ik=0L; ik < __target139984243176896; ik += 1L)
                  {
                    sov.fast(pythonic::types::make_tuple(ik, i0, i1)) = 0.0;
                  }
                }
              }
            }
          }
        }
      }
    }
    return pythonic::__builtin__::None;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_operators2d::__transonic__()());
typename __pythran_operators2d::compute_increments_dim1::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, long>::result_type compute_increments_dim10(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& var, long&& irx) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::compute_increments_dim1()(var, irx);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators2d::compute_increments_dim1::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, long>::result_type compute_increments_dim11(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& var, long&& irx) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::compute_increments_dim1()(var, irx);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators2d::invlaplacian_fft::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, long>::result_type invlaplacian_fft0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& a_fft, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& Kn_not0, long&& rank) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::invlaplacian_fft()(a_fft, Kn_not0, rank);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators2d::invlaplacian_fft::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, long>::result_type invlaplacian_fft1(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& a_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& Kn_not0, long&& rank) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::invlaplacian_fft()(a_fft, Kn_not0, rank);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators2d::invlaplacian_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, long>::result_type invlaplacian_fft2(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& a_fft, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& Kn_not0, long&& rank) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::invlaplacian_fft()(a_fft, Kn_not0, rank);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators2d::invlaplacian_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, long>::result_type invlaplacian_fft3(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& a_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& Kn_not0, long&& rank) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::invlaplacian_fft()(a_fft, Kn_not0, rank);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators2d::laplacian_fft::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type laplacian_fft0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& a_fft, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& Kn) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::laplacian_fft()(a_fft, Kn);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators2d::laplacian_fft::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type laplacian_fft1(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& a_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& Kn) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::laplacian_fft()(a_fft, Kn);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators2d::laplacian_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type laplacian_fft2(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& a_fft, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& Kn) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::laplacian_fft()(a_fft, Kn);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators2d::laplacian_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type laplacian_fft3(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& a_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& Kn) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::laplacian_fft()(a_fft, Kn);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsPseudoSpectral2D__dealiasing_setofvar = to_python(__pythran_operators2d::__code_new_method__OperatorsPseudoSpectral2D__dealiasing_setofvar()());
typename __pythran_operators2d::__for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar::type<bool, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar0(bool&& self__has_to_dealiase, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>&& self_where_dealiased, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& sov) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::__for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar()(self__has_to_dealiase, self_where_dealiased, sov);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators2d::__for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar::type<bool, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar1(bool&& self__has_to_dealiase, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>&& self_where_dealiased, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& sov) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators2d::__for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar()(self__has_to_dealiase, self_where_dealiased, sov);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_compute_increments_dim10(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"var","irx", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]))
        return to_python(compute_increments_dim10(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_increments_dim11(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"var","irx", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]))
        return to_python(compute_increments_dim11(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_invlaplacian_fft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"a_fft","Kn_not0","rank", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(invlaplacian_fft0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_invlaplacian_fft1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"a_fft","Kn_not0","rank", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(invlaplacian_fft1(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_invlaplacian_fft2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"a_fft","Kn_not0","rank", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(invlaplacian_fft2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_invlaplacian_fft3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"a_fft","Kn_not0","rank", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(invlaplacian_fft3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_laplacian_fft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"a_fft","Kn", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]))
        return to_python(laplacian_fft0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_laplacian_fft1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"a_fft","Kn", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]))
        return to_python(laplacian_fft1(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_laplacian_fft2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"a_fft","Kn", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]))
        return to_python(laplacian_fft2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_laplacian_fft3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"a_fft","Kn", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]))
        return to_python(laplacian_fft3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"self__has_to_dealiase","self_where_dealiased","sov", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<bool>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]))
        return to_python(__for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar0(from_python<bool>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"self__has_to_dealiase","self_where_dealiased","sov", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<bool>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]))
        return to_python(__for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar1(from_python<bool>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_increments_dim1(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_increments_dim10(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_increments_dim11(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_increments_dim1", "\n    - compute_increments_dim1(float64[:,:], int)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_invlaplacian_fft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_invlaplacian_fft0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_invlaplacian_fft1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_invlaplacian_fft2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_invlaplacian_fft3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "invlaplacian_fft", "\n    - invlaplacian_fft(complex128[:,:], float64[:,:], int)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_laplacian_fft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_laplacian_fft0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_laplacian_fft1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_laplacian_fft2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_laplacian_fft3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "laplacian_fft", "\n    - laplacian_fft(complex128[:,:], float64[:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar", "\n    - __for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar(bool, uint8[:,:], complex128[:,:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_increments_dim1",
    (PyCFunction)__pythran_wrapall_compute_increments_dim1,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the increments of var over the dim 1.\n\n    Supported prototypes:\n\n    - compute_increments_dim1(float64[:,:], int)"},{
    "invlaplacian_fft",
    (PyCFunction)__pythran_wrapall_invlaplacian_fft,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the n-th order inverse Laplacian.\n\n    Supported prototypes:\n\n    - invlaplacian_fft(complex128[:,:], float64[:,:], int)"},{
    "laplacian_fft",
    (PyCFunction)__pythran_wrapall_laplacian_fft,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the n-th order Laplacian.\n\n    Supported prototypes:\n\n    - laplacian_fft(complex128[:,:], float64[:,:])"},{
    "__for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar,
    METH_VARARGS | METH_KEYWORDS,
    "Dealiasing of a setofvar arrays.\n\n    Supported prototypes:\n\n    - __for_method__OperatorsPseudoSpectral2D__dealiasing_setofvar(bool, uint8[:,:], complex128[:,:,:])"},
    {NULL, NULL, 0, NULL}
};


            #if PY_MAJOR_VERSION >= 3
              static struct PyModuleDef moduledef = {
                PyModuleDef_HEAD_INIT,
                "operators2d",            /* m_name */
                "",         /* m_doc */
                -1,                  /* m_size */
                Methods,             /* m_methods */
                NULL,                /* m_reload */
                NULL,                /* m_traverse */
                NULL,                /* m_clear */
                NULL,                /* m_free */
              };
            #define PYTHRAN_RETURN return theModule
            #define PYTHRAN_MODULE_INIT(s) PyInit_##s
            #else
            #define PYTHRAN_RETURN return
            #define PYTHRAN_MODULE_INIT(s) init##s
            #endif
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(operators2d)(void)
            #ifndef _WIN32
            __attribute__ ((visibility("default")))
            __attribute__ ((externally_visible))
            #endif
            ;
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(operators2d)(void) {
                import_array()
                #if PY_MAJOR_VERSION >= 3
                PyObject* theModule = PyModule_Create(&moduledef);
                #else
                PyObject* theModule = Py_InitModule3("operators2d",
                                                     Methods,
                                                     ""
                );
                #endif
                if(! theModule)
                    PYTHRAN_RETURN;
                PyObject * theDoc = Py_BuildValue("(sss)",
                                                  "0.9.1post0",
                                                  "2019-03-07 11:14:52.140257",
                                                  "16c26fd1200d9ea4d9446923d3f149223904eae5c0ae526b54c6da7d237f9810");
                if(! theDoc)
                    PYTHRAN_RETURN;
                PyModule_AddObject(theModule,
                                   "__pythran__",
                                   theDoc);

                PyModule_AddObject(theModule, "__transonic__", __transonic__);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral2D__dealiasing_setofvar", __code_new_method__OperatorsPseudoSpectral2D__dealiasing_setofvar);
                PYTHRAN_RETURN;
            }

#endif