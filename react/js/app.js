class InfoBox extends React.Component {
	constructor() {
		super();
	}
	render(){
		let component = <InfoBoxContent small={this.props.title} />;
		
		if(this.props.component == "Reads"){
			component = <InfoBoxContentReads small={this.props.title} />;
		} else if (this.props.component == "MultiSession"){
			component = <InfoBoxContentMultiSession small={this.props.title} />;
		} else if (this.props.component == "TopArticles") {
			component = <InfoBoxContentTopArticles small={this.props.title} />;
		} else if (this.props.component == "Users"){
			component = <InfoBoxContentUsers small={this.props.title} />;
		} else if (this.props.component == "Visits"){
			component = <InfoBoxContentVisits small={this.props.title} />;
		}
		
		return (
			<div className="ibox float-e-margins">
        <div className="ibox-title">
          <span className="label label-success pull-right">To Date</span>
          <h5>{this.props.title}</h5>
        </div>
        {component}
      </div>
		)
	}
}

class InfoBoxContent extends React.Component {
	constructor() {
		super();

		this.state = {
			data: {}
		};
	}
	render(){
		const data = numeral(this._getData()).format('0,0')
		return (
      <div className="ibox-content">
        <h1 className="no-margins">{data}</h1>
        <div className="stat-percent font-bold text-success">0% <i className="fa fa-bolt"></i></div>
        <small>Total {this.props.small}</small>
      </div>
		)
	}
	componentWillMount(){
		this._fetchData();
	}
	componentDidMount(){
		this._timer = setInterval(() => this._fetchData(), 5000);
	}
	componentWillUnmount(){
		clearInterval(this._timer);
	}
	_fetchData() {
		return;
	}
	_getData(){
		return this.state.data.value;
	}
}

class InfoBoxContentUsers extends InfoBoxContent {
	_fetchData() {
		$.get("http://localhost:8888/api/total_users", {}, (data) => {
			this.setState({data});
		});
	}
}

class InfoBoxContentVisits extends InfoBoxContent {
	_fetchData() {
		$.get("http://localhost:8888/api/total_visits", {}, (data) => {
			this.setState({data});
		});
	}
}

class InfoBoxContentReads extends InfoBoxContent {
	render(){
		const data = numeral(this._getData()).format('0,0');
		return (
      <div className="ibox-content">
        <h1 className="no-margins">{data}</h1>
        <div className="font-bold text-navy">Reads: 0%  <i className="fa fa-bolt"></i> </div>
	    </div>
		)
	}
	_fetchData() {
		$.get("http://localhost:8888/api/total_reads", {}, (data) => {
			this.setState({data});
		});
	}
}

class InfoBoxContentTopArticles extends InfoBoxContent {
	render() {
		const data = this._getData() || [];

		return (
			<div className="ibox-content">
        <div className="row">  
          <div className="table-responsive">
            <table className="table table-striped">
              <thead>
                <tr>
                  <th>Article </th>
                  <th>Read Count </th>
                </tr>
              </thead>
              <tbody>
              	{data.map(article => {
              		return <Article data={article} key={article.id}/>
              	})}
              </tbody>
            </table>
          </div>
        </div>
      </div>
		)
	}

	_fetchData() {
		$.get("http://localhost:8888/api/top_read", {}, (data) => {
			this.setState({data});
		});
	}
}

class Article extends React.Component {
	render(){
		return (
			<tr>
        <td>{this.props.data.article_name}</td>
        <td>{this.props.data.read_count}</td>
      </tr>
    )
	}
}

class InfoBoxContentMultiSession extends React.Component {
	constructor(){
		super();
	}

	render() {
		return (
			<div className="ibox-content">
        <div className="m-t-sm">
          <div className="row">
            <div className="col-md-8">
              <div className="ibox-content">
                <div id="rickshaw_bars" className="rickshaw_graph"></div>
              </div>
            </div>
            <div className="col-md-4">
              <ul className="stat-list m-t-lg">
                <li>
                  <h2 className="no-margins">0</h2>
                  <small>Visitors who have multiple sessions (today)</small>
                  <div className="progress progress-mini">
                    <div className="progress-bar" style={{width: "48%"}}></div>
                  </div>
                </li>
                <li>
                  <h2 className="no-margins ">0</h2>
                  <small>Total sessions for the last 30 days</small>
                  <div className="progress progress-mini">
                    <div className="progress-bar" style={{width: "60%"}}></div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div className="m-t-md">
          <small className="pull-right">
            <i className="fa fa-clock-o"> </i>
            Updated on date
          </small>
          <small>
            <strong>Multi-session volume:</strong>Over the last 5 days, this shows your session count where users had more than 2 sessions
          </small>
        </div>
    	</div>
		)
	}
}

class App extends React.Component	{
	constructor() {
		super();
	}
	render() {
		return (
			<div id="page-wrapper" className="gray-bg">
			    <div className="row border-bottom">
			        <nav className="navbar navbar-static-top white-bg" role="navigation" style={{marginBottom: 0}}>
			            <div className="navbar-header">
			                <a className="navbar-minimalize minimalize-styl-2" href="#">
			                    <img src="../static/img/CBC-logo.jpg" height="25" />
			                </a>
			                <form role="search" className="navbar-form-custom" action="search_results.html">
			                    <div className="form-group">
			                        <input type="text" placeholder="Oh Hello there." className="form-control" name="top-search" id="top-search" />
			                    </div>
			                </form>
			            </div>
			            <ul className="nav navbar-top-links navbar-right">
			                <li>
			                    <span className="m-r-sm text-muted welcome-message">Welcome to CBC Graph.</span>
			                </li>
			                <li>
			                    <a href="http://cbc.ca">
			                        <i className="fa fa-sign-out"></i> Visit The CBC
			                    </a>
			                </li>
			            </ul>
			        </nav>
			    </div>
			    <div className="wrapper wrapper-content">
			        <div className="row">
			        		<div className="col-md-3">
	                	<InfoBox title="Users" component="Users" />
			            </div>
			            <div className="col-md-3">
			            	<InfoBox title="Visits" component="Visits" />
			            </div>
			            <div className="col-md-3">
			            	<InfoBox title="Reads" component="Reads" />
			            </div>
			            <div className="col-md-3">
		                <InfoBox title="30 Day Trend (FPO)" />
			            </div>
			        </div>
			        <div className="row">
			            <div className="col-lg-12">
			            	<InfoBox title="Muti-session views for the last n days" component="MultiSession"/>
			            </div>
			        </div>
			        <div className="row">
			            <div className="col-lg-12">
			            		<InfoBox title="Top Articles" component="TopArticles"/>
			            </div>
			        </div>
			        <div className="footer">
			            <div>
			                <strong>Copyright</strong> &copy; 2016 Propellerhead Labs
			            </div>
			        </div>
			    </div>
			</div>
		)
	}
}

ReactDOM.render(
	<App />,
	document.getElementById('wrapper')
);