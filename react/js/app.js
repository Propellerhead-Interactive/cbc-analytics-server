class InfoBox extends React.Component {
	constructor() {
		super();

		this.state = {
			articles: []
		};
	}

	_handleUserChange(data){
		this.setState({articles: data})
	}

	render(){
		let component = <InfoBoxContent small={this.props.title} />;
		let span = "To Date";
		let label_class = "label label-success pull-right";
		
		if(this.props.component == "Reads"){
			component = <InfoBoxContentReads small={this.props.title} />;
		} else if (this.props.component == "MultiSession"){
			component = <InfoBoxContentMultiSession small={this.props.title} />;
		} else if (this.props.component == "TopArticles") {
			component = <InfoBoxContentTopArticles small={this.props.title} articles={this.state.articles}/>;
		} else if (this.props.component == "Users"){
			component = <InfoBoxContentUsers small={this.props.title} />;
		} else if (this.props.component == "Visits"){
			component = <InfoBoxContentVisits small={this.props.title} />;
		} else if (this.props.component == "Content"){
			component = <InfoBoxContentContent small={this.props.title} />;
		} else if (this.props.component == "Sessions"){
			component = <InfoBoxContentSessions small={this.props.title} />;
		}

		if(this.props.span == 'select'){
			span = <DateSelector onUserChange={this._handleUserChange.bind(this)}/>;
			label_class = "pull-right";
		}
		
		return (
			<div className="ibox float-e-margins">
        <div className="ibox-title">
          <span className={label_class}>{span}</span>
          <h5>{this.props.title}</h5>
        </div>
        {component}
      </div>
		)
	}
}

class DateSelector extends React.Component {
	constructor(){
		super();
	}
	render(){
		return (
			<select className="date-selector" onChange={this._onChange.bind(this)}>
				<option value="">All</option>
				<option value={moment().subtract(1, 'days').format('x')}>In the last 24 hours</option>
				<option value={moment().subtract(2, 'days').format('x')}>In the last 48 hours</option>
				<option value={moment().subtract(7, 'days').format('x')}>In the last week</option>
				<option value={moment().subtract(1, 'month').format('x')}>In the last month</option>
			</select>
		)
	}
	_onChange(event){
		$.get("/api/top_read?date="+event.target.value, {}, (data) => {
			//this.setState({data});
			this.props.onUserChange(data);
		});
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
        {/*<div className="stat-percent font-bold text-success">0% <i className="fa fa-bolt"></i></div>
        <small>Total {this.props.small}</small> */}
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

class InfoBoxContentSessions extends InfoBoxContent {
	_fetchData() {
		$.get("/api/total_sessions", {}, (data) => {
			this.setState({data});
		});
	}
}

class InfoBoxContentContent extends InfoBoxContent {
	_fetchData() {
		$.get("/api/total_content", {}, (data) => {
			this.setState({data});
		});
	}
}

class InfoBoxContentUsers extends InfoBoxContent {
	_fetchData() {
		$.get("/api/total_users", {}, (data) => {
			this.setState({data});
		});
	}
}

class InfoBoxContentVisits extends InfoBoxContent {
	_fetchData() {
		$.get("/api/total_visits", {}, (data) => {
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
        {/*<div className="font-bold text-navy">Reads: 0%  <i className="fa fa-bolt"></i> </div> */}
	    </div>
		)
	}
	_fetchData() {
		$.get("/api/total_reads", {}, (data) => {
			this.setState({data});
		});
	}
}

class InfoBoxContentTopArticles extends InfoBoxContent {
	render() {
		const data = this.props.articles.value ? this.props.articles.value : this._getData() || [];

		return (
			<div className="ibox-content">
        <div className="row">  
          <div className="table-responsive">
            <table className="table table-striped">
              <thead>
                <tr>
                  <th>Article </th>
                  <th>Pubished On </th>
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
		$.get("/api/top_read", {}, (data) => {
			this.setState({data});
		});
	}
}

class Article extends React.Component {
	render(){
		return (
			<tr>
        <td><a href={this.props.data.url} target="_blank">{this.props.data.article_name}</a></td>
        <td>{moment.unix(this.props.data.publication_date/1000).format('YYYY/MM/DD')}</td>
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

		this.state = {
			read_pct: 5
		}
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
			        		<div className="col-md-4">
	                	<InfoBox title="Users" component="Users" />
			            </div>
			            <div className="col-md-4">
			            	<InfoBox title="Visits" component="Visits" />
			            </div>
			            <div className="col-md-4">
			            	<InfoBox title="Sessions" component="Sessions" />
			            </div>
			            {/*<div className="col-md-3">
		               //  <InfoBox title="30 Day Trend (FPO)" />
			             //</div>
			           	 */}
			        </div>
			        <h4>Content Relationship Counts</h4>
			        <div className="row">
			        	<div className="col-md-4">
                	<InfoBox title="Content" component="Content" />
		            </div>
		            <div className="col-md-4">
                	<InfoBox title="Reads" component="Reads" />
		            </div>
			        </div>
			        {/*
			        <div className="row">
			            <div className="col-lg-12">
			            	<InfoBox title="Muti-session views for the last n days" component="MultiSession"/>
			            </div>
			        </div>
			      	*/}
			      	<hr />
			        <div className="row">
			            <div className="col-lg-12">
			            		<InfoBox title="Top Articles" component="TopArticles" span="select"/>
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