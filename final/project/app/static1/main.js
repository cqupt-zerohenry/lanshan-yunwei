var host=window.location.host;
var url='http://'+host+'/metrics';
axios.get(url).then((response) => {
  let data = response.data; // 获取到的响应数据
  let cpudata = [{ value: parseFloat(data['CPU使用率']), name: 'CPU使用率' }];

  let memorydata = [
    { value: parseFloat(data['内存使用百分比']), name: '内存使用百分比' },
    { value: parseFloat(data['已用内存']), name: '已用内存' },
    { value: parseFloat(data['总内存']), name: '总内存' }
  ];
  let netdata = [
    { value: parseFloat(data['发送字节数']), name: '发送字节数' },
    { value: parseFloat(data['接收字节数']), name: '接收字节数' }
  ];
  let diskiodata = [
    { value: data['磁盘I/O信息']['读取字节数'], name: '读取字节数' },
    { value: data['磁盘I/O信息']['写入字节数'], name: '写入字节数' }
  ];

  // 创建Echarts实例并选取HTML元素
  let cpuChart = echarts.init(document.getElementById('cpuChart'));
  let memChart = echarts.init(document.getElementById('memChart'));
  let netChart = echarts.init(document.getElementById('netChart'));
  let diskIoChart = echarts.init(document.getElementById('diskIoChart'));

  // CPU信息
  cpuChart.setOption({
    title: {
      text: 'CPU信息',
      left: 'center',
      top: 'bottom'
    },
    series: [
      {
        type: 'gauge',
        data: cpudata,
        axisLine: {
          lineStyle: {
            color: [
              [0.6, '#91c7ae'],
              [0.8, '#63869e'],
              [1, '#c23531']
            ],
            width: 8
          }
        }
      }
    ]
  });

  // 内存信息
  memChart.setOption({
    color: ['#ffab91'],
    title: {
      text: '内存信息',
      left: 'center',
      top: 'bottom'
    },
    label: {
      show: true,
      position: 'top' // 在柱状图上显示数据标签
    },
    xAxis: {
      type: 'category',
      data: ['内存使用百分比', '已用内存', '总内存']
    },
    yAxis: {
      type: 'value'
    },
    series: [{ type: 'bar', data: memorydata.map((item) => item.value) }]
  });

  // 网络信息
  netChart.setOption({
    color: ['#b71c1c', '#4a148c'],
    title: {
      text: '网络信息',
      left: 'center',
      top: 'bottom'
    },
    series: [
      {
        type: 'pie',
        label: {
          show: true,
          position: 'outside',
          formatter: '{b} : {c} ({d}%)' // '{b}' 表示数据项的名称，'{c}' 表示数据项的值，'{d}' 表示该数据项在总数中的占比。
        },
        data: netdata
      }
    ]
  });

  // 磁盘IO信息
  diskIoChart.setOption({
    color: ['#ffcdd2', '#ce93d8'],
    title: {
      text: '磁盘IO信息',
      left: 'center',
      top: 'bottom'
    },
    series: [
      {
        type: 'pie',
        label: {
          show: true,
          position: 'outside',
          formatter: '{b} : {c} ({d}%)' // '{b}' 表示数据项的名称，'{c}' 表示数据项的值，'{d}' 表示该数据项在总数中的占比。
        },
        data: diskiodata
      }
    ]
  });
});
