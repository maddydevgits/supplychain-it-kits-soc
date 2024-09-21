// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract SupplyChain {
  address owner;
  struct product{
    uint id;
    string name;
    bool valid;
    address d;
    address r;
    bool isDistributed;
    bool isRetailed;
  }
  mapping(uint=>product) products;

  constructor() {
    owner=msg.sender;
  }

  // m-> products add
  function addProduct(uint i,string memory n) public{
    require(owner==msg.sender);
    // verify product exist
    require(!products[i].valid);
    // record create
    product memory new_product=product(i,n,true,owner,owner,false,false);
    // record map
    products[new_product.id]=new_product;
  }

  // d -> assign
  function addDistributor(uint i,address d) public{
    // product exist
    require(products[i].valid);
    require(!products[i].isDistributed);
    products[i].d=d;
    products[i].isDistributed=true;
  }

  // r -> assign
  function addRetailer(uint i,address r) public{
    require(products[i].valid);
    require(!products[i].isRetailed);
    products[i].r=r;
    products[i].isRetailed=true;
  }

  // product verify
  function verifyProduct(uint i) public view returns(product memory){
      return(products[i]);
  }
}
