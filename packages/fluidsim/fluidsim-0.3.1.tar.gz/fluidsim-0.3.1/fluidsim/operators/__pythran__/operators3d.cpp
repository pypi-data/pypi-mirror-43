#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/uint8.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/uint8.hpp>
#include <pythonic/include/__builtin__/None.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/types/complex.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/__builtin__/None.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/types/complex.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_operators3d
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
  struct dealiasing_variable
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
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
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& ff_fft, argument_type1&& where_dealiased) const
    ;
  }  ;
  struct dealiasing_setofvar
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
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
      typedef typename std::tuple_element<3,typename std::remove_reference<__type3>::type>::type __type16;
      typedef typename pythonic::lazy<__type16>::type __type17;
      typedef decltype(std::declval<__type1>()(std::declval<__type17>())) __type18;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type18>::type::iterator>::value_type>::type __type19;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type11>(), std::declval<__type15>(), std::declval<__type19>())) __type20;
      typedef __type0 __ptype4;
      typedef __type20 __ptype5;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& sov, argument_type1&& where_dealiased) const
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft
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
  struct __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type0;
      typedef std::complex<double> __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype((pythonic::operator_::mul(std::declval<__type2>(), std::declval<__type0>()))) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type5;
      typedef decltype((pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type5>()))) __type6;
      typedef decltype((pythonic::operator_::add(std::declval<__type3>(), std::declval<__type6>()))) __type7;
      typedef typename pythonic::assignable<decltype((pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type7>())))>::type __type8;
      typedef decltype((pythonic::operator_::mul(std::declval<__type8>(), std::declval<__type2>()))) __type9;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type10;
      typedef decltype((pythonic::operator_::mul(std::declval<__type9>(), std::declval<__type10>()))) __type11;
      typedef typename pythonic::assignable<decltype((std::declval<__type0>() - std::declval<__type11>()))>::type __type12;
      typedef decltype((pythonic::operator_::mul(std::declval<__type8>(), std::declval<__type4>()))) __type13;
      typedef decltype((pythonic::operator_::mul(std::declval<__type13>(), std::declval<__type10>()))) __type14;
      typedef typename pythonic::assignable<decltype((std::declval<__type5>() - std::declval<__type14>()))>::type __type15;
      typedef decltype((std::declval<__type0>() - std::declval<__type12>())) __type16;
      typedef decltype((std::declval<__type5>() - std::declval<__type15>())) __type17;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type12>(), std::declval<__type15>(), std::declval<__type16>(), std::declval<__type17>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_inv_K_square_nozero, argument_type3&& vx_fft, argument_type4&& vy_fft) const
    ;
  }  ;
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.1.11.post0"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 >
  typename dealiasing_variable::type<argument_type0, argument_type1>::result_type dealiasing_variable::operator()(argument_type0&& ff_fft, argument_type1&& where_dealiased) const
  {
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, ff_fft)))>::type n0 = std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, ff_fft));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, ff_fft)))>::type n1 = std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, ff_fft));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, ff_fft)))>::type n2 = std::get<2>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, ff_fft));
    {
      long  __target139984240253024 = n0;
      for (long  i0=0L; i0 < __target139984240253024; i0 += 1L)
      {
        {
          long  __target139984239432088 = n1;
          for (long  i1=0L; i1 < __target139984239432088; i1 += 1L)
          {
            {
              long  __target139984239432648 = n2;
              for (long  i2=0L; i2 < __target139984239432648; i2 += 1L)
              {
                if (where_dealiased.fast(pythonic::types::make_tuple(i0, i1, i2)))
                {
                  ff_fft.fast(pythonic::types::make_tuple(i0, i1, i2)) = 0.0;
                }
              }
            }
          }
        }
      }
    }
    return pythonic::__builtin__::None;
  }
  template <typename argument_type0 , typename argument_type1 >
  typename dealiasing_setofvar::type<argument_type0, argument_type1>::result_type dealiasing_setofvar::operator()(argument_type0&& sov, argument_type1&& where_dealiased) const
  {
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type nk = std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type n0 = std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type n1 = std::get<2>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov));
    typename pythonic::lazy<decltype(std::get<3>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type n2 = std::get<3>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, sov));
    {
      long  __target139984240273896 = n0;
      for (long  i0=0L; i0 < __target139984240273896; i0 += 1L)
      {
        {
          long  __target139984240275128 = n1;
          for (long  i1=0L; i1 < __target139984240275128; i1 += 1L)
          {
            {
              long  __target139984240251176 = n2;
              for (long  i2=0L; i2 < __target139984240251176; i2 += 1L)
              {
                if (where_dealiased.fast(pythonic::types::make_tuple(i0, i1, i2)))
                {
                  {
                    long  __target139984240252352 = nk;
                    for (long  ik=0L; ik < __target139984240252352; ik += 1L)
                    {
                      sov.fast(pythonic::types::make_tuple(ik, i0, i1, i2)) = 0.0;
                    }
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
  typename __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::type::result_type __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, vx_fft, vy_fft):\n"
"    return pythran_func(self.Kx, self.Ky, self.inv_K_square_nozero, vx_fft, vy_fft)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
  typename __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_inv_K_square_nozero, argument_type3&& vx_fft, argument_type4&& vy_fft) const
  {
    typename pythonic::assignable<decltype((pythonic::operator_::mul(std::complex<double>(0.0, 1.0), (pythonic::operator_::add((pythonic::operator_::mul(self_Kx, vx_fft)), (pythonic::operator_::mul(self_Ky, vy_fft)))))))>::type divh_fft = (pythonic::operator_::mul(std::complex<double>(0.0, 1.0), (pythonic::operator_::add((pythonic::operator_::mul(self_Kx, vx_fft)), (pythonic::operator_::mul(self_Ky, vy_fft))))));
    typename pythonic::assignable<decltype((vx_fft - (pythonic::operator_::mul((pythonic::operator_::mul(divh_fft, self_Kx)), self_inv_K_square_nozero))))>::type urx_fft = (vx_fft - (pythonic::operator_::mul((pythonic::operator_::mul(divh_fft, self_Kx)), self_inv_K_square_nozero)));
    typename pythonic::assignable<decltype((vy_fft - (pythonic::operator_::mul((pythonic::operator_::mul(divh_fft, self_Ky)), self_inv_K_square_nozero))))>::type ury_fft = (vy_fft - (pythonic::operator_::mul((pythonic::operator_::mul(divh_fft, self_Ky)), self_inv_K_square_nozero)));
    ;
    ;
    return pythonic::types::make_tuple(urx_fft, ury_fft, (vx_fft - urx_fft), (vy_fft - ury_fft));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_operators3d::__transonic__()());
typename __pythran_operators3d::dealiasing_variable::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long,long>>>::result_type dealiasing_variable0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& ff_fft, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long,long>>&& where_dealiased) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::dealiasing_variable()(ff_fft, where_dealiased);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators3d::dealiasing_setofvar::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long,long>>, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long,long>>>::result_type dealiasing_setofvar0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long,long>>&& sov, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long,long>>&& where_dealiased) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::dealiasing_setofvar()(sov, where_dealiased);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft = to_python(__pythran_operators3d::__code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft()());
typename __pythran_operators3d::__for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_inv_K_square_nozero, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::__for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft()(self_Kx, self_Ky, self_inv_K_square_nozero, vx_fft, vy_fft);
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
__pythran_wrap_dealiasing_variable0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"ff_fft","where_dealiased", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long,long>>>(args_obj[1]))
        return to_python(dealiasing_variable0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_dealiasing_setofvar0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"sov","where_dealiased", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long,long>>>(args_obj[1]))
        return to_python(dealiasing_setofvar0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"self_Kx","self_Ky","self_inv_K_square_nozero","vx_fft","vy_fft", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_dealiasing_variable(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_dealiasing_variable0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "dealiasing_variable", "\n    - dealiasing_variable(complex128[:,:,:], uint8[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_dealiasing_setofvar(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_dealiasing_setofvar0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "dealiasing_setofvar", "\n    - dealiasing_setofvar(complex128[:,:,:,:], uint8[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft", "\n    - __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft(float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "dealiasing_variable",
    (PyCFunction)__pythran_wrapall_dealiasing_variable,
    METH_VARARGS | METH_KEYWORDS,
    "Dealiasing 3d array\n\n    Supported prototypes:\n\n    - dealiasing_variable(complex128[:,:,:], uint8[:,:,:])"},{
    "dealiasing_setofvar",
    (PyCFunction)__pythran_wrapall_dealiasing_setofvar,
    METH_VARARGS | METH_KEYWORDS,
    "Dealiasing 3d setofvar object.\n\n    Supported prototypes:\n\n    - dealiasing_setofvar(complex128[:,:,:,:], uint8[:,:,:])\n\n    Parameters\n    ----------\n\n    sov : 4d ndarray\n        A set of variables array.\n\n    where_dealiased : 3d ndarray\n        A 3d array of \"booleans\" (actually uint8).\n\n"},{
    "__for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft,
    METH_VARARGS | METH_KEYWORDS,
    "Compute toroidal and poloidal horizontal velocities\n\n    Supported prototypes:\n\n    - __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft(float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:])\n\n"},
    {NULL, NULL, 0, NULL}
};


            #if PY_MAJOR_VERSION >= 3
              static struct PyModuleDef moduledef = {
                PyModuleDef_HEAD_INIT,
                "operators3d",            /* m_name */
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
            PYTHRAN_MODULE_INIT(operators3d)(void)
            #ifndef _WIN32
            __attribute__ ((visibility("default")))
            __attribute__ ((externally_visible))
            #endif
            ;
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(operators3d)(void) {
                import_array()
                #if PY_MAJOR_VERSION >= 3
                PyObject* theModule = PyModule_Create(&moduledef);
                #else
                PyObject* theModule = Py_InitModule3("operators3d",
                                                     Methods,
                                                     ""
                );
                #endif
                if(! theModule)
                    PYTHRAN_RETURN;
                PyObject * theDoc = Py_BuildValue("(sss)",
                                                  "0.9.1post0",
                                                  "2019-03-07 11:14:52.537151",
                                                  "8ddcd633b59af03efc7018e1c8875b35126edec281a51e2a4d3f424e06fe6313");
                if(! theDoc)
                    PYTHRAN_RETURN;
                PyModule_AddObject(theModule,
                                   "__pythran__",
                                   theDoc);

                PyModule_AddObject(theModule, "__transonic__", __transonic__);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft", __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft);
                PYTHRAN_RETURN;
            }

#endif