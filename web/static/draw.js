//from http://www.ourd3js.com/wordpress/?p=555

var drawing_relationship = function (data_url) {
    var width = 1024;
    var height = 768;
    var img_w = 77;
    var img_h = 90;

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);
    d3.json(data_url, function (error, root) {

        if (error) {
            return console.log(error);
        }
        console.log(root);

        var force = d3.layout.force()
            .nodes(root.nodes)
            .links(root.edges)
            .size([width, height])
            .linkDistance(200)
            .charge(-1500)
            .start();

        var edges_line = svg.selectAll("line")
            .data(root.edges)
            .enter()
            .append("line")
            .style("stroke", "#ccc")
            .style("stroke-width", 1);

        var edges_text = svg.selectAll(".linetext")
            .data(root.edges)
            .enter()
            .append("text")
            .attr("class", "linetext")
            .text(function (d) {
                return d.relation;
            });


        var nodes_img = svg.selectAll("image")
            .data(root.nodes)
            .enter()
            .append("image")
            .attr("width", img_w)
            .attr("height", img_h)
            .attr("xlink:href", function (d) {
                return d.image;
            })
            .on("mouseover", function (d, i) {
                //显示连接线上的文字
                edges_text.style("fill-opacity", function (edge) {
                    if (edge.source === d || edge.target === d) {
                        return 1.0;
                    }
                });
            })
            .on("mouseout", function (d, i) {
                //隐去连接线上的文字
                edges_text.style("fill-opacity", function (edge) {
                    if (edge.source === d || edge.target === d) {
                        return 0.0;
                    }
                });
            })
            .call(force.drag);

        var text_dx = -20;
        var text_dy = 20;

        var nodes_text = svg.selectAll(".nodetext")
            .data(root.nodes)
            .enter()
            .append("text")
            .attr("class", "nodetext")
            .attr("dx", text_dx)
            .attr("dy", text_dy)
            .text(function (d) {
                return d.name;
            });


        force.on("tick", function () {

            //限制结点的边界
            root.nodes.forEach(function (d, i) {
                d.x = d.x - img_w / 2 < 0 ? img_w / 2 : d.x;
                d.x = d.x + img_w / 2 > width ? width - img_w / 2 : d.x;
                d.y = d.y - img_h / 2 < 0 ? img_h / 2 : d.y;
                d.y = d.y + img_h / 2 + text_dy > height ? height - img_h / 2 - text_dy : d.y;
            });

            //更新连接线的位置
            edges_line.attr("x1", function (d) { return d.source.x; });
            edges_line.attr("y1", function (d) { return d.source.y; });
            edges_line.attr("x2", function (d) { return d.target.x; });
            edges_line.attr("y2", function (d) { return d.target.y; });

            //更新连接线上文字的位置
            edges_text.attr("x", function (d) { return (d.source.x + d.target.x) / 2; });
            edges_text.attr("y", function (d) { return (d.source.y + d.target.y) / 2; });


            //更新结点图片和文字
            nodes_img.attr("x", function (d) { return d.x - img_w / 2; });
            nodes_img.attr("y", function (d) { return d.y - img_h / 2; });

            nodes_text.attr("x", function (d) { return d.x });
            nodes_text.attr("y", function (d) { return d.y + img_w / 2; });
        });
    });
}

var drawing_piechart = function (data_url) {
    var width = 600;
    var height = 600;

    var svg = d3.select("body")			//选择<body>
        .append("svg")			//在<body>中添加<svg>
        .attr("width", width)	//设定<svg>的宽度属性
        .attr("height", height);//设定<svg>的高度属性

    d3.json(data_url, function (error, root) {
        if (error) {
            return console.log(error);
        }

        var dataset = root["data"];

        //2.转换数据
        var pie = d3.layout.pie()
            .value(function (d) { return d[1]; });

        var piedata = pie(dataset);

        console.log(piedata);

        //3.绘制

        //字体大小
        var fontsize = 14;

        //外半径和内半径
        var outerRadius = 400 / 3;
        var innerRadius = 0;

        //创建弧生成器
        var arc = d3.svg.arc()
            .innerRadius(innerRadius)
            .outerRadius(outerRadius);

        var color = d3.scale.category20();

        //添加对应数目的弧组，即<g>元素
        var arcs = svg.selectAll("g")
            .data(piedata)		//绑定转换后的数据piedata
            .enter()
            .append("g")
            .attr("transform", "translate(" + (outerRadius) + "," + (outerRadius) + ")");

        //绘制弧
        arcs.append("path")
            .attr("fill", function (d, i) {
                return color(i);	//设定弧的颜色
            })
            .attr("d", function (d) {
                return arc(d);	//使用弧生成器
            });


        //绘制弧内的文字
        arcs.append("text")
            .attr("transform", function (d) {
                var x = arc.centroid(d)[0] * 1.4;		//文字的x坐标
                var y = arc.centroid(d)[1] * 1.4;		//文字的y坐标
                return "translate(" + x + "," + y + ")";
            })
            .attr("text-anchor", "middle")
            .style("font-size", fontsize)
            .text(function (d) {
                //计算市场份额的百分比
                var percent = Number(d.value) / d3.sum(dataset, function (d) { return d[1]; }) * 100;

                //保留1位小数点，末尾加一个百分号返回
                return d.data[0] + " " + d.value + " (" + percent.toFixed(1) + "%)";
            });

    });
}