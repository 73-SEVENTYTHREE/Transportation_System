 var dataChina=[
             {name:"南海诸岛",value:0},
            {name: '北京', value: 11111},
            {name: '天津', value: 222},
            {name: '上海', value: 333},
            {name: '重庆', value: 444},
            {name: '河北', value: 555},
            {name: '河南', value: 666},
            {name: '云南', value: 311},
            {name: '辽宁', value: 233},
            {name: '黑龙江', value: 888},
            {name: '湖南', value: 777},
            {name: '安徽', value: 1057},
            {name: '山东', value: 80},
            {name: '新疆', value: 999},
            {name: '江苏', value: 318},
            {name: '浙江', value: 581},
            {name: '江西', value: 180},
            {name: '湖北', value: 317},
            {name: '广西', value: 600},
            {name: '甘肃', value: 250},
            {name: '山西', value: 521},
            {name: '内蒙古', value: 1517},
            {name: '陕西', value: 1777},
            {name: '吉林', value: 2990},
            {name: '福建', value: 100},
            {name: '贵州', value: 51},
            {name: '广东', value: 0},
            {name: '青海', value: 89},
            {name: '西藏', value: 976},
            {name: '四川', value: 546},
            {name: '宁夏', value: 338},
            {name: '海南', value: 220},
            {name: '台湾', value: 667},
            {name: '香港', value: 990},
            {name: '澳门', value: 880}
       ]
        var chinaChart = echarts.init(document.getElementById('main-chart'));

        option = {
            tooltip: {
                    formatter:function(params,ticket, callback){
                        return params.seriesName+'<br />'+params.name+'：'+params.value
                    }//数据格式化
                },
            visualMap: {
                min: 0,
                max: 1500,
                left: 'left',
                top: 'bottom',
                text: ['高','低'],//取值范围的文字
                inRange: {
                    color: ['#e0ffff', '#b22222']//取值范围的颜色
                },
                show:true//图注
            },
            geo: {
                map: 'china',
                roam: false,//不开启缩放和平移
                zoom:1.23,//视角缩放比例
                label: {
                    normal: {
                        show: true,
                        fontSize:'10',
                        color: 'rgba(0,0,0,0.7)'
                    }
                },
                itemStyle: {
                    normal:{
                        borderColor: 'rgba(0, 0, 0, 0.2)'
                    },
                    emphasis:{
                        areaColor: '#F3B329',//鼠标选择区域颜色
                        shadowOffsetX: 0,
                        shadowOffsetY: 0,
                        shadowBlur: 20,
                        borderWidth: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            },
            series : [
                {
                    name: '日增加人数',
                    type: 'map',
                    geoIndex: 0,
                    data:dataChina
                }
            ]
        };
        chinaChart.setOption(option);
        chinaChart.on('click', function (params) {
            alert(params.name);
        });

