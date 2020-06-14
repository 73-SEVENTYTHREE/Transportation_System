var dataBeijing=[
            {name: '东城区', value: 88},
            {name: '西城区', value: 99},
            {name: '朝阳区', value: 151},
            {name: '丰台区', value: 121},
            {name: '石景山区', value: 191},
            {name: '海淀区', value: 777},
            {name: '门头沟区', value: 3},
            {name: '房山区', value: 11},
            {name: '通州区', value: 50},
            {name: '顺义区', value: 177},
            {name: '昌平区', value: 0},
            {name: '大兴区', value: 543},
            {name: '怀柔区', value: 331},
            {name: '平谷区', value: 223},
            {name: '密云区', value: 18},
            {name: '延庆区', value: 0}
        ]
        var BeijingChart = echarts.init(document.getElementById('beijing-chart'));

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
                map: '北京',
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
                    data:dataBeijing
                }
            ]
        };
        BeijingChart.setOption(option);
        BeijingChart.on('click', function (params) {
            alert(params.name);
        });// JavaScript Document