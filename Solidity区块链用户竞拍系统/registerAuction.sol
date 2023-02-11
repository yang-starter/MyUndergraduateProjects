pragma solidity ^0.4.23;

contract registerAuction {

    address public beneficiary;    //受益者账户地址

    event NewUser(uint id, string name, uint age);   //定义事件

    string public projectDescription;  //该次拍卖项目的描述
    

    // 时间是unix的绝对时间戳（自1970-01-01以来的秒数）
    //或以秒为单位的时间段。
    uint public auctionEndtime;  //竞拍结束时间
    
    // 判断拍卖是否进行的状态
    bool isAuction = false;
    //防止拍卖重复开始的状态
    bool auctionStarted = false;

    address public highestBidder;    //最高出价者
    uint public highestBid;    //最高出价
    //存储注册用户地址的数列
    uint[128] addrList;
    mapping(address => uint) pendingReturns;


    event HighestBidIncreased(address bidder, uint amount);
    event AuctionEnded(address winner, uint amount);

    struct User {       //结构体
        string name;
        uint age;
    }


    User[] public users;    //结构数组

    mapping(uint => User) idToUser;    //映射，建立 id号 到 用户基本信息 的映射

   

    constructor (
        uint _biddingTime,
        string _projectDescription,
        address _beneficiary
    )  public {
        projectDescription = _projectDescription;  //保存项目的描述
        beneficiary = _beneficiary;   //拍卖发起者账户地址
        auctionEndtime = block.timestamp + _biddingTime;    //竞拍时长
    }

    //注册用户的基本信息 
    function registerUser(uint _id, string _name, uint _age) public {
        users.push(User({name:_name, age:_age}));
        idToUser[_id] = users[users.length - 1];    
        emit NewUser(_id, _name, _age);    //触发事件

        for (uint i = 0; i < addrList.length; i++) {
            if(addrList[i] == 0){
                addrList[i] = _id;
                break;
            }
        }
    }

    //获取用户的基本信息 
    function getUser(uint _id) external view returns(string name, uint age) {
        User storage user = idToUser[_id];
        (name, age) = (user.name, user.age);
    }


    //注册完毕之后开始拍卖，并且防止重复开始
    function startAuction() public {
        require( auctionStarted == false, "Auction already started.");
        isAuction = true;
        
    }

    function bid() public payable {
        // 如果拍卖已结束，撤销函数的调用。
        bool isinarray = false;
        require( block.timestamp <= auctionEndtime, "Auction already ended.");
        require( isAuction == true, "cannot bid now.");
        auctionStarted = true;
        // 如果出价不够高，返还你的钱
        require( msg.value > highestBid, "There already is a higher bid.");
        // 防止虚空用户竞价
        for (uint i = 0; i < addrList.length; i++) {
            if(addrList[i] == uint(msg.sender)){
                isinarray = true;
            }
        }
        require( isinarray == true,"Please sign in first next time!");
        // 之前的最高出价者收回出价
        highestBidder.transfer(highestBid);
        // 最高出价和最高出价者的转移
        highestBidder = msg.sender;
        highestBid = msg.value;
        emit HighestBidIncreased(msg.sender, msg.value);
    }


    function endAuction() public{
        // 对于可与其他合约交互的函数（意味着它会调用其他函数或发送以太币）
        // 一个好的指导方针是将其结构分为三个阶段：
        // 1. 检查条件
        // 2. 执行动作 (可能会改变条件)
        // 3. 与其他合约交互

        // 1. 条件
        require(block.timestamp >= auctionEndtime, "Auction not yet ended.");
        // 2. 生效
        isAuction = false;
        emit AuctionEnded(highestBidder, highestBid);
        // 3. 交互
        beneficiary.transfer(highestBid);
    }
    function gethighestbidder() external view returns (string name, uint age, uint bidnum){
        // 竞价结束后进行查询
        require(isAuction == false,"Auction not yet ended.");

        User storage user = idToUser[uint(highestBidder)];
        (name, age) = (user.name, user.age);
        bidnum = highestBid;
    }

}