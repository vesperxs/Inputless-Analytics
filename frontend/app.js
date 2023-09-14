import G6 from '@antv/g6';
import insertCss from 'insert-css';
import './styles.js';
//import { EyeFilled } from '@ant-design/icons-svg';

//import  {appIcons} from "ionicons/icons";
import {list} from "ionicons/icons";
let active_nodes = {
    'PERSON'	: true,
    'ARTICOLI'	: true,
    'DECRETI' 	: true,
    'FILENAMES' : true,
    'LOCATION' : true,
    'CASSAZIONE' : true,
    'IDPROC' 	: true
};


const div = document.getElementById("div");
div.id = 'mountNode';


const width = div.scrollWidth || 2000;
const height = div.scrollHeight || 1500;

//get the structure from django
const data2 = (document.getElementById("data").textContent === '') ? 
      null : JSON.parse(document.getElementById("data").textContent);

//---------------------------------------------------------------------
const menuContainer = document.createElement('div');
const tagUl = document.createElement('ul');

const tagCheck = document.createElement('input');
const tagCheck2 = document.createElement('input');
const tagCheck3 = document.createElement('input');
//const tagCheck4 = document.createElement('input');
const tagCheck5 = document.createElement('input');
const tagCheck6 = document.createElement('input');
const tagCheck7 = document.createElement('input');

const tagLabel = document.createElement('label');
const tagLabel2 = document.createElement('label');
const tagLabel3 = document.createElement('label');
//const tagLabel4 = document.createElement('label');
const tagLabel5 = document.createElement('label');
const tagLabel6 = document.createElement('label');
const tagLabel7 = document.createElement('label');

menuContainer.className = "sidebar";
div.appendChild(menuContainer); //anchor to the root div
menuContainer.appendChild(tagUl);

tagLabel.innerHTML = 'PERSON  ';
tagLabel2.innerHTML = 'ARTICOLI';
tagLabel3.innerHTML = 'DECRETI';
//tagLabel4.innerHTML = 'FILENAMES';
tagLabel5.innerHTML = 'LOCATION';
tagLabel6.innerHTML = 'CASSAZIONE';
tagLabel7.innerHTML = 'IDPROC';

tagCheck.type = 'checkbox';
tagCheck.click();
tagCheck.id = 'mycheckbox';
tagUl.appendChild(tagCheck);
tagUl.appendChild(tagLabel);

tagCheck2.type = 'checkbox';
tagCheck2.click();
tagCheck2.id = 'mycheckbox2';
tagUl.appendChild(tagCheck2);
tagUl.appendChild(tagLabel2);

tagCheck3.type = 'checkbox';
tagCheck3.click();
tagCheck3.id = 'mycheckbox3';
tagUl.appendChild(tagCheck3);
tagUl.appendChild(tagLabel3);

// tagCheck4.type = 'checkbox';
// tagCheck4.id = 'mycheckbox4';
// tagUl.appendChild(tagCheck4);
// tagUl.appendChild(tagLabel4);

tagCheck5.type = 'checkbox';
tagCheck5.click();
tagCheck5.id = 'mycheckbox5';
tagUl.appendChild(tagCheck5);
tagUl.appendChild(tagLabel5);

tagCheck6.type = 'checkbox';
tagCheck6.click();
tagCheck6.id = 'mycheckbox6';
tagUl.appendChild(tagCheck6);
tagUl.appendChild(tagLabel6);

tagCheck7.type = 'checkbox';
tagCheck7.click();
tagCheck7.id = 'mycheckbox7';
tagUl.appendChild(tagCheck7);
tagUl.appendChild(tagLabel7);

//show-hide button
const tagB = document.createElement('a');
tagB.className = "btn";
div.appendChild(tagB);


const button = document.querySelector('.btn'),
      sidebar = document.querySelector('.sidebar');


button.innerHTML = `${list}`;

tagCheck.addEventListener('click', function () {
    if (active_nodes['PERSON'] === true) make_invisible('PERSON');
    else (make_visible('PERSON'));
});
tagCheck2.addEventListener('click', function () {
    if (active_nodes['ARTICOLI'] === true) make_invisible('ARTICOLI');
    else (make_visible('ARTICOLI'));
});
tagCheck3.addEventListener('click', function () {
    if (active_nodes['DECRETI'] === true) make_invisible('DECRETI');
    else (make_visible('DECRETI'));
});
// tagCheck4.addEventListener('click', function () {
// 	if (active_nodes['FILENAMES'] === true) make_invisible('FILENAMES');
// 	else (make_visible('FILENAMES'))
// });
tagCheck5.addEventListener('click', function () {
    if (active_nodes['LOCATION'] === true) make_invisible('LOCATION');
    else (make_visible('LOCATION'));
});
tagCheck6.addEventListener('click', function () {
    if (active_nodes['CASSAZIONE'] === true) make_invisible('CASSAZIONE');
    else (make_visible('CASSAZIONE'));
});
tagCheck7.addEventListener('click', function () {
    if (active_nodes['IDPROC'] === true) make_invisible('IDPROC');
    else (make_visible('IDPROC'));
});

button.addEventListener('click', function () {
    button.classList.toggle('btnc');
    sidebar.classList.toggle('side');
});
//--------------------------------------------------------------------


const legendContainer = document.createElement('div');
legendContainer.id = 'legendContainer';
const legendGraphDiv = document.createElement('div');
legendGraphDiv.id = 'legend';
legendContainer.appendChild(legendGraphDiv);
div.parentNode.appendChild(legendContainer);
const legendGraph = new G6.Graph({
    container: 'legend',
    width: 150,
    height: 150,
    defaultNode: {
	size: 10,
	type: 'circle',
	labelCfg: {
	    position: 'right',
	    offset: 10,
	    style: {
		fill: '#000',
	    },
	},
    },
});

const legendX = 20;
const legendBeginY = 50;
const legendYPadding = 25;
const legendData = {
    nodes: [
	{
	    id: 'level1',
	    x: legendX,
	    y: legendBeginY,
	    label: 'DOCUMENT',
	    style: {
		fill: '#260026',
		lineWidth: 0,
	    },
	},
	{
	    id: 'level2',
	    x: legendX,
	    y: legendBeginY + 15,
	    label: 'PERSON',
	    style: {
		fill: '#F6C3B7',
		lineWidth: 0,
	    },
	},
	{
	    id: 'level3',
	    label: 'ID PROCESSO',
	    x: legendX,
	    y: legendBeginY + 30,
	    style: {
		fill: '#BDEFDB',
		lineWidth: 0,
	    },
	},
	{
	    id: 'level4',
	    label: 'ARTICOLO',
	    x: legendX,
	    y: legendBeginY + 45,
	    style: {
		fill: '#BDD2FD',
		lineWidth: 0,
	    },
	},
        {
	    id: 'level5',
	    label: 'DECRETO',
	    x: legendX,
	    y: legendBeginY + 60,
	    style: {
		fill: '#FFD8B2',
		lineWidth: 0,
	    },
	},
        {
	    id: 'level6',
	    label: 'CASSAZIONE',
	    x: legendX,
	    y: legendBeginY + 75,
	    style: {
		fill: '#FFD8B8',
		lineWidth: 0,
	    },
	},
    ],
};

legendGraph.data(legendData);
legendGraph.render();

const minimap = new G6.Minimap();
const toolbar = new G6.ToolBar();

const tooltip = new G6.Tooltip({
    offsetX: 10,
    offsetY: 10,
    trigger: 'click',
    // the types of items that allow the tooltip show up
    itemTypes: ['node', 'edge'],
    // custom the tooltip's content
    getContent: (e) => {
	const outDiv = document.createElement('mountNode');
	outDiv.style.width = 'fit-content';
	//outDiv.style.padding = '0px 0px 20px 0px';
	outDiv.innerHTML = `
      <h4>Custom Content</h4>
	    <ul>
            <li>Typess: ${e.item.getType()}</li>
	    </ul>
	    <ul>
            <li>Label: ${e.item.getModel().label || e.item.getModel().id}</li>
	    </ul>`;
	return outDiv;
    },
});


let colorMap = {
    DECRETI: '#FFD8B2',
    ARTICOLI: '#BDD2FD',
    IDPROC: '#BDEFDB',
    PERSON: '#F6C3B7',
    CASSAZIONE: '#FFD8B8',
    LOCATION: '#D3C6EA',
    FILENAME: '#F08BB4',
};

const duration = 2000;
const animateOpacity = 0.6;
const animateBackOpacity = 0.1;
const virtualEdgeOpacity = 0.1;
const realEdgeOpacity = 0.2;


const subjectColors = [
    '#5F95FF', // blue
    '#F08BB4', //filename
    '#65789B',
    '#F6BD16',
    '#7262FD',
    '#78D3F8',
    '#9661BC',
    '#F6903D',
    '#008685',
    '#F08BB4',
];

const colorSets = G6.Util.getColorSetsBySubjectColors(
    subjectColors,
);

const fittingString = (str, maxWidth, fontSize) => {
    let currentWidth = 0;
    let res = str;
    const pattern = new RegExp('[\u4E00-\u9FA5]+'); // distinguish the Chinese charactors and letters
    str.split('').forEach((letter, i) => {
	if (currentWidth > maxWidth) return;
	if (pattern.test(letter)) {
	    // Chinese charactors
	    currentWidth += fontSize;
	} else {
	    // get the width of single letter according to the fontSize
	    currentWidth += G6.Util.getLetterWidth(letter, fontSize);
	}
	if (currentWidth > maxWidth) {
	    res = `${str.substr(0, i)}\n${str.substr(i)}`;
	}
    });
    return res;
};


G6.registerNode(
    'aggregated-node', {
	draw(cfg, group) {
	    let width = 120, height = 80;
	    const style = cfg.style || {};
	    const colorSet = cfg.colorSets || colorSets[6];
	    
	    const keyShape = group.addShape('rect', {
		attrs: {
		    ...style,
		    x: -width / 2,
		    y: -height / 2,
		    width,
		    height,
		    fill: '#993f69',
		    stroke: colorSet.mainStroke,
		    lineWidth: 2,
		    cursor: 'pointer',
		    radius: height / 2 || 13,
		},
		name: 'aggregated-node-keyShape',
	    });
	    
	    let labelStyle = {};
	    if (cfg.labelCfg) {
		labelStyle = Object.assign(labelStyle, cfg.labelCfg.style);
	    }
	    group.addShape('text', {
		attrs: {
		    text: `${cfg.label}`,
		    x: 0,
		    y: 0,
		    textAlign: 'center',
		    textBaseline: 'middle',
		    cursor: 'pointer',
		    fontSize: 12,
		    fill: '#fff',
		    opacity: 0.85,
		    fontWeight: 400,
		},
		name: 'count-shape',
		className: 'count-shape',
		draggable: true,
	    });
	    
	    
	    return keyShape;
	},
		
	update: undefined,
    },
    'single-node',
);
// Custom real node
const global = {
    node: {
	style: {
	    fill: '#2B384E',
	},
	labelCfg: {
	    style: {
		fill: '#acaeaf',
		stroke: '#191b1c',
	    },
	},
	stateStyles: {
	    focus: {
		fill: '#2B384E',
	    },
	},
    },
    edge: {
	style: {
	    stroke: '#acaeaf',
	    realEdgeStroke: '#acaeaf', //'#f00',
	    realEdgeOpacity,
	    strokeOpacity: realEdgeOpacity,
	},
	labelCfg: {
	    style: {
		fill: '#acaeaf',
		realEdgeStroke: '#acaeaf', //'#f00',
		realEdgeOpacity: 0.5,
		stroke: '#191b1c',
	    },
	},
	stateStyles: {
	    focus: {
		stroke: '#fff', // '#3C9AE8',
	    },
	},
    },
};


G6.registerNode(
    'real-node',
    {
	draw(cfg, group) {
	    let r = 30;
	    const style = cfg.style || {};
	    const colorSet = cfg.colorSet || colorSets[0];

	    // halo for hover
	    group.addShape('circle', {
		attrs: {
		    x: 0,
		    y: 0,
		    r: r + 5,
		    fill:  '#2B384E',
		    opacity: 0.9,
		    lineWidth: 0,
		},
		name: 'halo-shape',
		visible: false,
	    });

	    // focus stroke for hover
	    group.addShape('circle', {
		attrs: {
		    x: 0,
		    y: 0,
		    r: r + 5,
		    fill:  '#2B384E',
		    stroke: '#fff',
		    strokeOpacity: 0.85,
		    lineWidth: 1,
		},
		name: 'stroke-shape',
		visible: false,
	    });

	    const keyShape = group.addShape('circle', {
		attrs: {
		    ...style,
		    x: 0,
		    y: 0,
		    r,
		    fill: '#2B384E',
		    stroke: colorSet.mainStroke,
		    lineWidth: 2,
		    cursor: 'pointer',
		},
		name: 'aggregated-node-keyShape',
	    });

	    let labelStyle = {};
	    if (cfg.labelCfg) {
		labelStyle = Object.assign(labelStyle, cfg.labelCfg.style);
	    }

	    if (cfg.label) {
		const text = cfg.label;
		let labelStyle = {};
		let refY = 0;
		if (cfg.labelCfg) {
		    labelStyle = Object.assign(labelStyle, cfg.labelCfg.style);
		    refY += cfg.labelCfg.refY || 0;
		}
		let offsetY = 0;
		const fontSize = labelStyle.fontSize < 8 ? 8 : labelStyle.fontSize;
		const lineNum = cfg.labelLineNum || 1;
		offsetY = lineNum * (fontSize || 12);
		group.addShape('text', {
		    attrs: {
			text,
			x: 0,
			y: r + refY + offsetY + 5,
			textAlign: 'center',
			textBaseLine: 'alphabetic',
			cursor: 'pointer',
			fontSize,
			fill: '#fff',
			opacity: 0.85,
			fontWeight: 400,
			stroke: global.edge.labelCfg.style.stroke,
		    },
		    name: 'text-shape',
		    className: 'text-shape',
		});
	    }

	    // tag for new node
	    if (cfg.new) {
		group.addShape('circle', {
		    attrs: {
			x: r - 3,
			y: -r + 3,
			r: 4,
			fill: '#6DD400',
			lineWidth: 0.5,
			stroke: '#FFFFFF',
		    },
		    name: 'typeNode-tag-circle',
		});
	    }

	    return keyShape;
	},
	
	update: undefined,
    },
    'aggregated-node',
); 


G6.registerEdge(
    'line-growth',
    {
	setState: (name, value, item) => {
	    const group = item.get('group');
	    const model = item.getModel();
	},
	afterDraw(cfg, group) {
	    const shape = group.get('children')[0];
	    const length = shape.getTotalLength();
	    shape.animate(
		(ratio) => {
		    // the operations in each frame. Ratio ranges from 0 to 1 indicating the prograss of the animation. Returns the modified configurations
		    const startLen = ratio * length;
		    // Calculate the lineDash
		    const cfg = {
			lineDash: [startLen, length - startLen],
		    };
		    return cfg;
		},
		{
		    repeat: true, // Whether executes the animation repeatly
		    duration: 1200, // the duration for executing once
		},
	    );
	},
    },
    'edge-shape', // extend the built-in edge 'cubic'
);

const ConcentricLayout = (() => {
    graph.updateLayout({
	type: 'concentric',
	nodeSpacing:70,
	minNodeSpacing: 50,
	preventOverlap: true,
	preventNodeOverlap:true,

    });
});

const ForceLayout = (() => {
    graph.updateLayout({
	type:'force',
	preventOverlap: true,
	preventNodeOverlap:true,
	gravity: 0.1,
	minNodeSpacing: 50,
	//unitRadius:400,
	linkDistance: 39,
	nodeSpacing:50,
	nodeStrength: 0.1,
	edgeStrength:0.1,
	
    });
});
const DagreLayout = (() => {
    graph.updateLayout({
	type: 'dagre',
	nodesep: 20,
	ranksep: 150,
    });
});
const CircularLayout = (() => {
    graph.updateLayout({
	type:'circular',
	preventOverlap: true,
	preventNodeOverlap:true,
	//gravity: 0.1,
	//unitRadius:400,
	//nodeSpacing:3000,
	//minNodeSpacing: 3000,
	
	//linkDistance: 2000,
	//nodeSpacing:2000,
	divisions: 10,
	radius: 700,
	startAngle: Math.PI / 4,
	endAngle: Math.PI,
    });
});

const RadialLayout = (() => {
    graph.updateLayout({
	type: 'radial',
	preventOverlap: true,
	preventNodeOverlap:true,
	//gravity: 0.2,
	unitRadius:400,
	groupNodes:true,
	
	linkDistance: 2000,
	nodeSpacing:1000*2,
	//nodeStrength: 60,
	//edgeStrength:0.3,

    });
});

const hideItem = ((e, deleteRoot, leaveCorrelation) => {
    const first = e._cfg.model;
    const item = e.item;
    const model = e.getModel();
    let non_zero_counter = 0; //VIENE INCREMENTATA SE IL NODO E' STATO GENERATO DA UN NODO PRESENTE O CI SONO NODI COLLEGATI CHE SONO STATI ESPANSI
    //SE DIVERSO DA 0 ALLORA POSSO ELIMINARE IL NODO IN QUESTIONE IN QUANTO E' ISOLATO, SE NON E' ROOT
    if (model.expanded === true){ //EVITA DI ELIMINARE NODI PADRI PARTENDO DA NODI FIGLI
	const curEdges = [];
	const edgesToHide = [];
	//console.log("clicked");
	const edges = graph.getEdges();
	curEdges.push(e._cfg.edges);

	curEdges.forEach((e) => {
	    const len = e.length;
	    for (let i = 0; i < len; i++) {
		edgesToHide.push(e[i]._cfg);
	    };
	});

	for (let i = 0; i < edgesToHide.length; i++){
	    if(model.type != 'aggregated-node'){
		//console.log(edgesToHide[i]);
		if(edgesToHide[i].model.mamt === model.id){ //CONTROLLO CHE IL NODO FIGLIO SIA STATO GENERATO DAL NODO IN QUESTIONE
		    let counter = 0;
		    for(let x = 0; x < edges.length; x++){
			if(edges[x]._cfg.model.source === edgesToHide[i].model.source)
			    counter++;
		    }
		    if(counter === 1){ //SE IL NODO FIGLIO E' UN NODO ISOLATO
			graph.removeItem(edgesToHide[i].model.id);
			const elem = graph.findById(edgesToHide[i].model.source);
			if (elem._cfg.model.isRoot === false){ //ELIMINO IL NODO SOLO SE NON E' ROOT
			    graph.removeItem(edgesToHide[i].model.source);
			}

		    }
		    else if (leaveCorrelation ===false){ //SE IL NODO HA PIU' COLLEGAMENTI ELIMINO SOLO L'EDGE E NON IL NODO CHE RESTERA' UNITO AGLI ALTRI NODI COLLEGATI
			non_zero_counter++;
			const elem = graph.findById(edgesToHide[i].model.source);
			console.log(edgesToHide[i].model.source);

			//hideItem(elem, true, false) 					//LA RICORSIONE PERMETTE DI ELIMINARE IL NODO COLLEGATO AL NODO SU CUI SI E' CLICCATO
			//E TUTTI I SUOI SOTTONODI, SE DISATTIVATO ELIMINA IL COLLEGAMENTO MA LASCIA INTATTA
			//LA STRUTTURA DI ELEM(NODO COLLEGATO A MODEL MA A SUA VOLTA ESPANSO)

			//inserire la condizione con deleteRoot===TRUE se vuoi eliminare il nodo figlio espanso
			graph.removeItem(edgesToHide[i].model.id);
			if (elem.expanded === true && elem.isRoot === false){
			    graph.removeItem(elem.id);
			}
		    }
		}
		else non_zero_counter++;
	    }
	    else {
		if(edgesToHide[i].model.mamt === model.id){
		    let counter = 0;
		    for(let x = 0; x < edges.length; x++){
			if(edges[x]._cfg.model.target === edgesToHide[i].model.target)
			    counter++;
		    }
		    if(counter === 1){
			graph.removeItem(edgesToHide[i].model.id);
			const elem = graph.findById(edgesToHide[i].model.target);
			if (elem._cfg.model.isRoot === false){
			    graph.removeItem(edgesToHide[i].model.target);
			}
		    }
		    else if (leaveCorrelation ===false){
			non_zero_counter ++;
			const elem = graph.findById(edgesToHide[i].model.target);
			//hideItem(elem, true, false)
			graph.removeItem(edgesToHide[i].model.id);
			if (elem.expanded === true && elem.isRoot === false){
			    graph.removeItem(elem.id);
			}
		    }
		}
		else non_zero_counter++;
	    }
	}
	if (leaveCorrelation===false) model.expanded = false;
	if (non_zero_counter == 0 && model.isRoot === false) graph.removeItem(model.id);
    }
    
    graph.layout();
});


const expandNodes = ((model) => {
    
    const itemModel = model;
    const nodes = graph.getNodes();
    const edges = graph.getEdges();
    const nodeLimit = 10;
    let newData = [];

    
    if (data2[itemModel.id].nodes.length > 1 || itemModel.isRoot === true){

	newData = data2[itemModel.id];

	const newNodeModels = newData.nodes;
	const newEdgeModels = [];

	newData.edges.forEach(function (e) {
	    let exist = false;
	    newEdgeModels.forEach(function (ne) {
		if (ne.source === e.source && ne.target === e.target) exist = true;
	    });
	    if (!exist) {
		e.mamt = itemModel.id;
		newEdgeModels.push(e);
	    }
	});
	//console.log(newEdgeModels); 
	
	// for graph.changeData()
	const allNodeModels = [],
	      allEdgeModels = [];
	
	// add new nodes to graph
	const nodeMap = new Map();
	nodes.forEach((n) => {
	    const nModel = n.getModel();
	    nodeMap.set(nModel.id, n);
	});
	newNodeModels.forEach((nodeModel) => {
	    if (nodeMap.get(nodeModel.id) === undefined) {
		// set the initial positions of the new nodes to the focus(clicked) node
		nodeModel.x = itemModel.x;
		nodeModel.y = itemModel.y;
		if (active_nodes[nodeModel.type] === false)
		    console.log('newNodeModels');
		graph.addItem('node', nodeModel);
	    }
	    
	});
	
	// add new edges to graph
	const edgeMap = new Map();
	edges.forEach(function (e, i) {
	    const eModel = e.getModel();
	    edgeMap.set(eModel.source + ',' + eModel.target, i);
	});
	const oldEdgeNum = edges.length;
	newEdgeModels.forEach(function (em, i) {
	    const exist = edgeMap.get(em.source + ',' + em.target);
	    if (exist === undefined) {
		graph.addItem('edge', em);
		edgeMap.set(em.source + ',' + em.target, oldEdgeNum + i);
	    }
	});

	edges.forEach((e) => {
	    allEdgeModels.push(e.getModel());
	});
	nodes.forEach((n) => {
	    allNodeModels.push(n.getModel());
	});

	// NOTE: for every elements assign its  node type
	
	allNodeModels.forEach((i) => {
	    //SOSTITUIRE CON UN CASE PER OGNI TIPOLOGIA
	    if(i.type === 'FILENAME') { 
		i.type = 'aggregated-node';
	    }
	    //else if (i.type === 'PERSON') {
	    // i.type = 'real-node';
	    //}
	    //console.log(i.cluster);
	    //i.cluster = i.type;
	    i.style = Object.assign(i.style || {}, {
		fill: colorMap[i.type],
		
	    });
	});
	graph.data({
	    nodes: allNodeModels,
	    edges: allEdgeModels,
	});
	
	graph.render();
	model.expanded = true;
	define_edge_types();
    }
    graph.getEdges().forEach(function (edge) {
	var s_type = edge._cfg.model.source.split('/')[0];
	var t_type = edge._cfg.model.target.split('/')[0];
	if (active_nodes[s_type] === false || active_nodes[t_type] === false)
	    edge.hide();
    });
    graph.getNodes().forEach(function (node) {
	if (active_nodes[node._cfg.model.type] === false)
	    node.hide();
    });

});

const highlight_correlations = function() {
    const edges = graph.getEdges();
    let edges_to_modify = [];

    for (let x=0; x<edges.length;x++)
    {
	let counter=0;
	for(let t =0; t<edges.length;t++){
	    if(edges[x]._cfg.model.target === edges[t]._cfg.model.target)
		counter++;
	}
	if(counter > 1) {
	    //edges_to_modify.push(edges[x]);
	    graph.updateItem(edges[x], {
		// update the edge style
		//custom-quadratic
		type: 'line-growth',
		style: {
		    startArrow:true,
		    endArrow: {
	    		path: 'M 0,0 L 8,4 L 8,-4 Z'
		    },
		    d: 10,
	    	    opacity: 7,
		    stroke: '#BDEFD4'
		    
		},//style
	    });//graph
	}
    }
}

const make_invisible = function(type_to_hide){
    if (active_nodes[type_to_hide] === true){
	const nodes = graph.getNodes();
	const edges = graph.getEdges();
	nodes.forEach((n)=>{
	    if(n._cfg.model.type === type_to_hide){
		n.hide();
		edges.forEach((e)=>{
		    if(e._cfg.model.target == n._cfg.model.id || e._cfg.model.source == n._cfg.model.id)
			e.hide();
		});
	    }
	});
	active_nodes[type_to_hide] = false;
    }
    const nodes = graph.getNodes();
}

const make_visible = function(type_to_show){
    if (active_nodes[type_to_show] === false){
	
	    const nodes = graph.getNodes();
	    const edges = graph.getEdges();
	    nodes.forEach((n)=>{
		if(n._cfg.model.type === type_to_show){
		    n.show();
		    edges.forEach((e)=>{
			if(e._cfg.model.target == n._cfg.model.id || e._cfg.model.target == n._cfg.model.id)
			    e.show();
		    });
		}
	    });
	    active_nodes[type_to_show] = true;
	}
}


const define_edge_types = function() {
    const edges = graph.getEdges();
    let edges_to_modify = [];

    for (let x=0; x<edges.length;x++)
    {
	let counter=0;
	for(let t =0; t<edges.length;t++){
	    if(edges[x]._cfg.model.target === edges[t]._cfg.model.target)
		counter++;
	}
	if(counter > 1) {
	    //edges_to_modify.push(edges[x]);
	    graph.updateItem(edges[x], {
		// update the edge style
		//custom-quadratic
		type: 'line',
		style: {
		    startArrow:true,
		    endArrow: {
	    		path: 'M 0,0 L 8,4 L 8,-4 Z'
		    },
		    d: 10,
	    	    opacity: 7,
		    stroke: '#F08BB4'
		    
		},//style
	    });//graph
	}//if
	
	else {
	    graph.updateItem(edges[x], {
		// update the edge style
		type: 'line',
		style: {
		    endArrow: {
	    		path: 'M 0,0 L 8,4 L 8,-4 Z'
		    },
		    //d: 6,
		    size:3,
	    	    fill: '#e2e2e2',
	    	    opacity: 4,
		    stroke: '#e2e2e2'
		},
	    });
	}
	
    }

};

const menu = new G6.Menu({

    getContent(evt) {
	    const { item } = evt;
	
	    if (evt.target && evt.target.isCanvas && evt.target.isCanvas()) {
		return `<ul>
            <li id='show'>Show all Hidden Items</li>
			<li id='collapseAll'>Collapse all Clusters</li>
			</ul>`;
	    } else if (!item) return;
	    const itemType = item.getType();
	    const model = item.getModel();
	    if (itemType && model) {
		if (itemType === 'node') {
		    if (model.type === 'aggregated-node') { //Documento
			return `<ul>
			<li id='expand'>Expand the Cluster</li>
			<li id='hide'>Reduce the Cluster</li>
			<li id='correlation'>Leave Correlations</li>
			<li id='updateForce'>Force Layout</li>
			<li id='updateCircular'>Circular Layout</li>
			<li id='updateConcentric'>Concentric layout</li>
			<li id='updateRadial'>Radial layout</li>
			<li id='updateDagre'>Dagre layout</li>
			</ul>`;
		    } else {
			return `<ul>
			<li id='neighbor-1'>Find 1-degree Neighbors</li>
			<li id='hide'>Hide the Node</li>
			<li id='correlation'>Leave Correlation</li>
			<li id='highlight_correlations'>Highlight Correlations</li>
			</ul>`;
		    }
		} else {
		    return `<ul>
			<li id='hide_person'>Hide Person Nodes</li>
			<li id='show_person'>Show Person Nodes</li>
			<li id='hide_location'>Hide Location Nodes</li>
			<li id='show_location'>Show Location Nodes</li>
			<li id='hide_arts'>Hide Articles Nodes</li>
			<li id='show_arts'>Show Articles Nodes</li>


			</ul>`;
		}
	    }
    },
    
    handleMenuClick(target, item) {
	const model = item && item.getModel();
	//console.log(item);
	const liIdStrs = target.id.split('-');
	//console.log(liIdStrs);
	switch(liIdStrs[0]) {
	case 'expand':
	    expandNodes(model);
	    break;
	case 'hide':
	    hideItem(item, false, false);
	    break;
	case 'correlation':
	    hideItem(item, false, true);
	    break;
	case 'highlight_correlations':
	    highlight_correlations();
	    break;
	case 'updateForce':
	    ForceLayout();
	    break;
	case 'updateCircular':
	    CircularLayout();
	    break;
	case 'updateConcentric':
	    ConcentricLayout();
	    break;
	case 'updateRadial':
	    RadialLayout();
	    break;
	case 'updateDagre':
	    DagreLayout();
	    break;
	case 'neighbor':
	    expandNodes(model);
	    break;
	case 'hide_person':
	    make_invisible('PERSON');
	    break;
	case 'hide_location':
	    make_invisible('LOCATION');
	    break;
	case 'hide_arts':
	    make_invisible('ARTICOLI');
	    break;
	case 'show_person':
	    make_visible('PERSON');
	    break;
	case 'show_location':
	    make_visible('LOCATION');
	    break;
	case 'show_arts':
	    make_visible('ARTICOLI');
	    break;
	default: break;
	}
    },
    
});

const graph = new G6.Graph({
    
    container: 'mountNode', // String | HTMLElement, required, the id of DOM element or an HTML node
    width, // centra il graph
    height, // Number, required, the height of the graph
    //fitWiew:true,
    fitCenter:true,
    fitViewPadding: [ 20, 40, 50, 20],
    linkCenter: false, //le frecce non puntano al centro
    //maxZoom:30,
    defaultNode: {
	/* node type */
	type: 'circle',
	/* node size */
	size: [60],
	/* style for the keyShape */
	style: {
	    //fill: '#9EC9FF',
	    stroke: '#5B8FF9',
	    lineWidth: 3,
	    // },
	    labelCfg: {
		/* label's position, options: center, top, bottom, left, right */
		position: 'bottom',
		/* label's offset to the keyShape, 4 by default */
		//   offset: 12,
		/* label's style */
		//   style: {
		//     fontSize: 20,
		//     fill: '#ccc',
		//     fontWeight: 500
	    }
	}

    },
    animate: true,
    workerEnabled: true,

    layout: {
	type: 'radial', //dagre, circular, force, fruchterman'
	preventOverlap: true,
	preventNodeOverlap:true,
	//gravity: 0.2,
	unitRadius:400,
	groupNodes:true,
	
	linkDistance: 2000,
	nodeSpacing:1000*2,
	//nodeStrength: 60,
	//edgeStrength:0.3,

	
    },
    animate: true,
    
    defaultEdge: {
	//type:'line-growth'
	size: 3,
	color: '#e2e2e2',
	style: {
	    endArrow: {
		path: 'M 0,0 L 8,4 L 8,-4 Z',
		d: 5,
		//fill: '#f00',
		//stroke: '#0f0',
		//opacity: 0.9,
		lineWidth: 7,
	    },
	},
    },
    

    modes: 
    {
	default: 
	['drag-node','drag-canvas','click-select','zoom-canvas',]},
    plugins: [menu,toolbar,tooltip,minimap,] //timebar,fisheye
});

//console.log(data2);
if(data2) {
    const data = data2['root'];


    graph.data({
	nodes:data.nodes,
	//edges: data.edges.map((edge, i) => {
	//      edge.id = `edge${i}`;
	//      return Object.assign({}, edge);
	//    }),
    });

    data.nodes.forEach((i) => {
	if(i.type === 'FILENAME') { 
	    i.type = 'aggregated-node';
	} 

	i.style = Object.assign(i.style || {}, {
	    fill: colorMap[i.type],
	});
    });

    graph.render();
}







graph.on('node:dragstart', function (e) {
    graph.layout();
    refreshDragedNodePosition(e);
});


graph.on('node:drag', function (e) {
    refreshDragedNodePosition(e);
    });
    graph.on('node:dragend', function (e) {
	e.item.get('model').fx = null;
	e.item.get('model').fy = null;
    });

    function refreshDragedNodePosition(e) {
	const model = e.item.get('model');
	model.fx = e.x;
	model.fy = e.y;
    }

    function clearAllStats() {
	graph.setAutoPaint(false);
	graph.getNodes().forEach(function (node) {
	    graph.clearItemStates(node);
	});
	graph.getEdges().forEach(function (edge) {
	    graph.clearItemStates(edge);
	});
	graph.paint();
	graph.setAutoPaint(true);
    }

    graph.on('node:mouseenter', function (e) {
	const item = e.item;
	graph.setAutoPaint(false);
	graph.getNodes().forEach(function (node) {
	    graph.clearItemStates(node);
	    graph.setItemState(node, 'dark', true);
	});

	graph.setItemState(item, 'dark', true);
	graph.setItemState(item, 'highlight', true);

    

    
	graph.getEdges().forEach(function (edge) {
	    if (edge.getSource() === item) {
		graph.setItemState(edge.getTarget(), 'dark', true);
		graph.setItemState(edge.getTarget(), 'highlight', true);
		graph.setItemState(edge, 'highlight', true);
		edge.toFront();
	    
	    } else if (edge.getTarget() === item) {
		graph.setItemState(edge.getSource(), 'dark', true); //mod
		graph.setItemState(edge.getSource(), 'highlight', true);
		graph.setItemState(edge, 'highlight', true);
		edge.toFront();
	    } else {
		graph.setItemState(edge, 'highlight', false); //mod
	    }
	});
	graph.paint();
	graph.setAutoPaint(true);
    });
    graph.on('node:click', function (e) {
	const node = e.item;
	const states = node.getStates();
	let clicked = false;
	const model = node.getModel();
	//let size = 200;
	let labelText =  model.label;
	states.forEach(function (state) {
	    if (state === 'click') {
		clicked = true;
		//size = model.size;// = 100;
		labelText = model.label;
	    }
	});
	graph.setItemState(node, 'click', !clicked);
	graph.updateItem(node, {
	    //size,
	    label: labelText,
	});
	graph.layout();
    });

    graph.on('node:mouseleave', clearAllStats);
    graph.on('canvas:click', clearAllStats);


    if (typeof window !== 'undefined')
	window.onresize = () => {
	    if (!graph || graph.get('destroyed')) return;
	    if (!div || !div.scrollwidth || !div.scrollheight) return;
	    graph.changesize(div.scrollwidth, div.scrollheight);
	};

