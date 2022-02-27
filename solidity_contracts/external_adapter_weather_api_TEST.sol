// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

contract externalAdapterWeatherAPI_TEST is ChainlinkClient, ConfirmedOwner {
    using Chainlink for Chainlink.Request;

    uint256 public value;

    uint256 constant private ORACLE_PAYMENT = 1 * LINK_DIVISIBILITY;

    event RequestWeatherFulfilled(
        bytes32 indexed requestId,
        uint256 indexed result
    );


    constructor() ConfirmedOwner(msg.sender){
    	setPublicChainlinkToken();
    	//fee = 0.1 * 10 ** 18; // 0.1 LINK
    }

    /**
     * Make initial request
     */
    function requestWeatherByCity(address _oracle, string memory _jobId,
        string memory _cityName,
        string memory _field)
    public
    onlyOwner
    {
    	Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), address(this), this.fulfillWeatherReq.selector);
    	req.add("city_name", _cityName);
        req.add("field", _field);
        req.add("path", "result");
        req.addInt("times", 100);
    	sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
    }

    function requestWeatherByCityAndStateCode(address _oracle, string memory _jobId,
        string memory _cityName,
        string memory _stateCode,
        string memory _field)
    public
    onlyOwner
    {
    	Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), address(this), this.fulfillWeatherReq.selector);
    	req.add("city_name", _cityName);
        req.add("state_code", _stateCode);
        req.add("field", _field);
        req.add("path", "result");
        req.addInt("times", 100);
    	sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
    }

    function requestWeatherByCityAndStateCodeCountryCode(address _oracle, string memory _jobId,
        string memory _cityName,
        string memory _stateCode,
        string memory _countryCode,
        string memory _field)
    public
    onlyOwner
    {
    	Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), address(this), this.fulfillWeatherReq.selector);
    	req.add("city_name", _cityName);
        req.add("state_code", _stateCode);
        req.add("country_code", _countryCode);
        req.add("field", _field);
        req.add("path", "result");
        req.addInt("times", 100);
    	sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
    }

    function requestWeatherByCityId(address _oracle, string memory _jobId,
        string memory _cityId,
        string memory _field)
    public
    onlyOwner
    {
    	Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), address(this), this.fulfillWeatherReq.selector);
    	req.add("city_id", _cityId);
        req.add("field", _field);
        req.add("path", "result");
        req.addInt("times", 100);
    	sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
    }

    function requestWeatherByLatAndLon(address _oracle, string memory _jobId,
        string memory _lat,
        string memory _lon,
        string memory _field)
    public
    onlyOwner
    {
    	Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), address(this), this.fulfillWeatherReq.selector);
    	req.add("lat", _lat);
        req.add("lon", _lon);
        req.add("field", _field);
        req.add("path", "result");
        req.addInt("times", 100);
    	sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
    }

    function requestWeatherByZipAndCountryCode(address _oracle, string memory _jobId,
        string memory _zipCode,
        string memory _countryCode,
        string memory _field)
    public
    onlyOwner
    {
    	Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), address(this), this.fulfillWeatherReq.selector);
    	req.add("zip_code", _zipCode);
        req.add("country_code", _countryCode);
        req.add("field", _field);
        req.add("path", "result");
        req.addInt("times", 100);
    	sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
    }

    /**
     * Callback function
     */
    function fulfillWeatherReq(bytes32 _requestId, uint256 _result)
    public
    recordChainlinkFulfillment(_requestId)
    {
        emit RequestWeatherFulfilled(_requestId, _result);
        value = _result;
    }

    function withdrawLink() public onlyOwner {
        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
        require(link.transfer(msg.sender, link.balanceOf(address(this))), "Unable to transfer");
    }

    function stringToBytes32(string memory source)
    private pure returns (bytes32 result)
    {
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
        return 0x0;
        }
        assembly { // solhint-disable-line no-inline-assembly
        result := mload(add(source, 32))
        }
    }
}
