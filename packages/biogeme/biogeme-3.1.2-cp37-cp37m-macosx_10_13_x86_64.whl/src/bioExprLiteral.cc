//-*-c++-*------------------------------------------------------------
//
// File name : bioExprLiteral.cc
// @date   Thu Apr 12 11:33:32 2018
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#include "bioExprLiteral.h"
#include <sstream>
#include "bioExceptions.h"
#include "bioDebug.h"

bioExprLiteral::bioExprLiteral(bioUInt literalId, bioString name) : bioExpression(), theLiteralId(literalId), theName(name),first(true),myId(bioBadId),theType(bioExprLiteral::bioUnknown) {
  
}
bioExprLiteral::~bioExprLiteral() {
}


bioDerivatives* bioExprLiteral::getValueAndDerivatives(std::vector<bioUInt> literalIds,
						       bioBoolean gradient,
						       bioBoolean hessian) {

  if (!gradient && hessian) {
    throw bioExceptions(__FILE__,__LINE__,"If the hessian is needed, the gradient must be computed") ;
  }

  if (theDerivatives == NULL) {
    theDerivatives = new bioDerivatives(literalIds.size()) ;
  }
  else {
    if (gradient && theDerivatives->getSize() != literalIds.size()) {
      delete(theDerivatives) ;
      theDerivatives = new bioDerivatives(literalIds.size()) ;
    }
  }

  
  
  if (gradient) {
    if (hessian) {
      theDerivatives->setDerivativesToZero() ;
    }
    else {
      theDerivatives->setGradientToZero() ;
    }
    for (std::size_t i = 0 ; i < literalIds.size() ; ++i) {
      if (literalIds[i] == theLiteralId) {
	theDerivatives->g[i] = 1.0 ;
      }
      else {
	theDerivatives->g[i] = 0.0 ;
      }
    }
  }
  theDerivatives->f = getLiteralValue() ;
  return theDerivatives ;
}


bioString bioExprLiteral::print() const {
  std::stringstream str ;
  str << theName << "[" << theLiteralId << "]" ;
  if (rowIndex != NULL) {
    str << " <" << *rowIndex << ">" ;
  }
  return str.str() ;
}

bioReal bioExprLiteral::getLiteralValue() {
  if (first) {
    first = false ;
    if (parameters == NULL) {
      throw bioExceptNullPointer(__FILE__,__LINE__,"parameters") ;
    }
    if (fixedParameters == NULL) {
      throw bioExceptNullPointer(__FILE__,__LINE__,"fixedParameters") ;
    }
    if (data == NULL) {
      throw bioExceptNullPointer(__FILE__,__LINE__,"data") ;
    }
    if (data->empty()) {
      throw bioExceptions(__FILE__,__LINE__,"No data") ;
    }
    if (theLiteralId >= (*data)[0].size() + parameters->size() + fixedParameters->size()) {
      std::stringstream str ;
      str << theName << ": " << theLiteralId << " out of range [0," << (*data)[*rowIndex].size() + parameters->size() + fixedParameters->size() - 1 << "]" ;
      throw bioExceptions(__FILE__,__LINE__,str.str()) ;
    }
    myId = theLiteralId ;
    // The numbering is sequential. First the parameters, then the fixed parameters, then the variables
    if (myId >= parameters->size()) {
      myId -= parameters->size() ;
      if (myId >= fixedParameters->size()) {
	myId -= fixedParameters->size() ;
	theType = bioExprLiteral::bioVariable ;
      }
      else {
	theType = bioExprLiteral::bioFixedParameter ;
      }
    }
    else {
      theType = bioExprLiteral::bioParameter ;
    }
  }
  switch(theType) {
  case bioVariable:
    if (rowIndex == NULL) {
      throw bioExceptNullPointer(__FILE__,__LINE__,"row index") ;
    }
    if (*rowIndex >= data->size()) {
      std::stringstream str ;
      str << theName << ": " << *rowIndex << " out of range [0," << data->size() - 1 << "]" ;
      throw bioExceptions(__FILE__,__LINE__,str.str()) ;
      
    }
    if (myId >= (*data)[*rowIndex].size()) {
      throw bioExceptOutOfRange<bioUInt>(__FILE__,__LINE__,myId,0,(*data)[*rowIndex].size() - 1) ;
    }
    return (*data)[*rowIndex][myId] ;
  case bioFixedParameter:
    if (myId >= fixedParameters->size()) {
      throw bioExceptOutOfRange<bioUInt>(__FILE__,__LINE__,myId,0,fixedParameters->size()  - 1) ;
    }
    return (*fixedParameters)[myId] ;
  case bioParameter:
    if (myId >= parameters->size()) {
      throw bioExceptOutOfRange<bioUInt>(__FILE__,__LINE__,myId,0,parameters->size() - 1) ;
    }
    return (*parameters)[myId] ;
  default:
    std::stringstream str ;
    str << "Unknown literal type: " << theType ;
    throw bioExceptions(__FILE__,__LINE__,str.str()) ;
  }
}

bioBoolean bioExprLiteral::containsLiterals(std::vector<bioUInt> literalIds) const {
  for (std::vector<bioUInt>::const_iterator i = literalIds.begin() ;
       i != literalIds.end() ;
       ++i) {
    if (*i == theLiteralId) {
      return true ;
    }
  }
  return false ;
}

void bioExprLiteral::setData(std::vector< std::vector<bioReal> >* d) {
  data = d ;
}


std::map<bioString,bioReal> bioExprLiteral::getAllLiteralValues() {
  std::map<bioString,bioReal> m ;
  m[theName] = getLiteralValue() ;
  return m ;
}
