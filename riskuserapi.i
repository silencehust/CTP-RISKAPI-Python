%module(directors="1") riskuserapi

%{
#include <iostream>
#include <string>
#include <boost/locale.hpp>
#include "FtdcRiskUserApi.h"
%}

%feature("doxygen:ignore:system", range="line");
%feature("doxygen:ignore:company", range="line");
%feature("doxygen:ignore:history", range="line");
%feature("doxygen:ignore:file", range="line");
// %feature("doxygen:ignore:brief", range="line");
%feature("doxygen:alias:d{8}") "\d{8}"
%feature("doxygen:alias:d{4}") "\d{4}"
%feature("doxygen:alias:d{3}") "\d{3}"
%feature("doxygen:alias:d{1}") "\d{1}"

%feature("python:annotations", "c");
%feature("director") CShfeFtdcRiskUserSpi;

%typemap(out) char[ANY], char[] {
    if ("$1_name" == "Content" && "$symname" == "CThostFtdcSettlementInfoField_Content_get") {
        $result = PyBytes_FromString($1);
    } else {
        if ($1){
            if (!strlen($1)) {
                $result = SWIG_FromCharPtr("");
            } else {
                const std::string utf8_str = std::move(boost::locale::conv::to_utf<char>($1, "GBK"));
                $result = SWIG_FromCharPtrAndSize(utf8_str.c_str(),utf8_str.size());
            }
        }
    }
}

%typemap(out) char {
    if ($1 == '\0'){
        $result = SWIG_FromCharPtr("");
    } else {
        char tmp[2]={0};
        sprintf(tmp, "%c", $1);
        $result = SWIG_FromCharPtr(tmp);
    }
}

%feature("director:except") {
  if ($error != NULL) {
    if (PyErr_ExceptionMatches(PyExc_SystemExit)) {
      throw Swig::DirectorMethodException("Exception: SystemExit");
    } else if (PyErr_ExceptionMatches(PyExc_SystemError)) {
      throw Swig::DirectorMethodException("Exception: SystemError");
    } else {
      PyErr_Print();
    }
  }
}

%ignore SHFE_FTDC_VTC_BankBankToFuture;
%ignore SHFE_FTDC_VTC_BankFutureToBank;
%ignore SHFE_FTDC_VTC_FutureBankToFuture;
%ignore SHFE_FTDC_VTC_FutureFutureToBank;
%ignore SHFE_FTDC_FTC_BankLaunchBankToBroker;
%ignore SHFE_FTDC_FTC_BrokerLaunchBankToBroker;
%ignore SHFE_FTDC_FTC_BankLaunchBrokerToBank;
%ignore SHFE_FTDC_FTC_BrokerLaunchBrokerToBank;


%include "FtdcRiskUserApiDataType.h"
%include "FtdcRiskUserApiStruct.h"
%include "FtdcRiskUserApi.h"
