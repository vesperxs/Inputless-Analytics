
import insertCss from 'insert-css';

import   "ionicons/icons";
insertCss(`
	.g6-component-contextmenu {
	border: 1px solid #ececec;
	border-radius: 4px;
	font-size: 15px;
	color: #ececec;
	background-color:rgb(2 4 14 / 74%);
	padding: 10px 8px;
	box-shadow: rgb(174, 174, 174) 0px 0px 10px;
    }
	  .g6-contextmenu-ul {
	      padding: 0;
	      margin: 0;
	      list-style: none;
	  }


	  .g6-component-toolbar {
	      position: absolute;
	      list-style-type: none;
	      padding: 14px;
	      left: -92px;
	      top: 226px;
	      background-color: rgb(122 164 255 / 42%);
	      border: 1px solid #e2e2e2;
	      border-radius: 4px;
	      font-size: 12px;
	      color: #545454;
	      margin: 0;
              transform:rotate(90deg);
	  }
	  .g6-component-toolbar li {
	      float: left;
	      text-align: center;
	      width: 35px;
	      height: 24px;
	      cursor: pointer;
	      list-style-type:none;
	      list-style: none;
	      margin-left: 0px;
	  }
	  .g6-component-toolbar li .icon {
	      opacity: 0.7;
	  }
	  .g6-component-toolbar li .icon:hover {
	      opacity: 1;
	  }

	  .g6-component-tooltip {
	      border: 1px solid #e2e2e2;
	      border-radius: 4px;
	      font-size: 12px;
	      color: #545454;
	      background-color: rgb(2 2 14 / 74%);
	      padding: 10px 8px;
	      box-shadow: rgb(174, 174, 174) 0px 0px 10px;
	  }
	  .tooltip-type {
	      padding: 0;
	      margin: 0;
	  }
	  .tooltip-id {
	      color: #531dab;
	  }
	  g6-component-contextmenu {
	      position: absolute;
	      z-index: 2;
	      list-style-type: none;
	      background-color: coral;
	      border-radius: 6px;
	      font-size: 14px;
	      color: rgba(156, 110, 110, 0.85);
	      width: fit-content;
	      transition: opacity .2s;
	      text-align: center;
	      padding: 0px 20px 0px 20px;
	      box-shadow: 0 5px 18px 0 rgba(0, 0, 0, 0.6);
	      border: 0px;
	  }
	  .g6-component-contextmenu ul {
	      padding-left: 0px;
	      margin: 0;
	  }
	  .g6-component-contextmenu li {
	      cursor: pointer;
	      list-style-type: none;
	      list-style: none;
	      margin-left: 0;
	      line-height: 38px;
	  }
	  .g6-component-contextmenu li:hover {
	      color: #363b40
	  }
         
         #legendContainer{
            position: absolute;
	    list-style-type: none;
	    padding: -3px;
            left: 4px;
            top: 1075px;
            background-color: rgb(122 164 255 / 42%);
            border: 1px solid #e2e2e2;
            border-radius: 4px;
            font-size: 12px;
            color: #545454;
           }

.sidebar {
  float: left;
  width: 600px;
  /* height: 70px; */
  margin-left: -3000px;
  background: #0b131959;
  overflow: hidden;
  transition: .8s all;
}

.side {
  margin-left: 0px;
}

.sidebar ul {
  margin: 8px;
  padding: 3px;
}

.sidebar ul li {
  list-style: none;
}
ol, ul, dl {
    margin-top: 0;
     margin-bottom: 1rem;
}

.sidebar ul li a {
  text-decoration: none;
  color: white;
  height: 80px;
  width: 100%;
  font-size: 40px;
  line-height: 80px;
  text-align: center;
  display: block;
  transition: .6s all;
}

.sidebar ul li a:hover {
  background: #34495e;
}

.btn {
  float: left;
  padding: 18 23px;
  text-decoration: none;
  color: #2c3e50;
  font-family: Ionicons;
  cursor: pointer;
  /*position: absolute;*/
	 }

a.btn {
    border: 0px solid transparent;
    font-size: 0;
}

a.btn svg {
    height: 62px;
    margin: -14px 0em;
}

input, button, select, optgroup, textarea {
    /* margin: 0; */
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
}




`);
