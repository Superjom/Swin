#include <iostream>
#include <string>
using namespace std;

#define LIST_H_

typedef struct{
    string data;
    long hashvalue;
}Node;

class List{
 private:
    vector<Node> list;
 public:
    int GetSize();
    int Insert(int i, long hashvalue, string data);
    //取得url中str
    string GetUrlsStr();
    void Show();
    int Find(long hashvalue);
};

int List::GetSize()
{
    return this->list.size()
}

int List::Insert(int i, Node node)
{
    if (i > this->GetSize() || i < 0) return false;
    UrlNode burl;
    burl = node
    int j = this->GetSize();
    //添加一个空间
    this->list.push_back(burl)
    while(j>i)
    {
        this->list[j] = this->list[j-1];
        --j;
    }

    this->list[i] = burl;
    return true;
}
//将其中的urllist转化为一个字符串
string List::ReturnUrlsStr()
{
    int size = this->GetSize()
    string res;
    for(int i=0; i<size; i++)
    {
        res += this->list[i];
    }
    return res;
}





