/**
 * Created by meixuhong on 9/10/16.
 */

/*
 我身在何处？

 先给数组排序，然后找到指定的值在数组的位置，最后返回位置对应的索引。

 举例：where([1,2,3,4], 1.5) 应该返回 1。因为1.5插入到数组[1,2,3,4]后变成[1,1.5,2,3,4]，而1.5对应的索引值就是1。

 同理，where([20,3,5], 19) 应该返回 2。因为数组会先排序为 [3,5,20]，19插入到数组[3,5,20]后变成[3,5,19,20]，而19对应的索引值就是2。

 */

function where(arr, num) {
    // Find my place in this sorted array.

    arr.push(num);

    //说明: sort内部的函数名isLarger也可以省略不写
    arr.sort(function isLarger(a,b) {
        return a - b;
    });

    console.log("arr:",arr,arr.indexOf(num));
    return arr.indexOf(num);
}

where([40, 60,1,10,70,23,24], 2);
