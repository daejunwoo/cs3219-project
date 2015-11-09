var React = require('react');
var Dropzone = require('react-dropzone');
var superagent = require('superagent');

var Router = require('react-router').Router;
var Route = require('react-router').Route;
var Link = require('react-router').Link;
var History = require('react-router').History;
var Lifecycle = require('react-router').Lifecycle;

var createHistory = require('history').createHistory;
var useBasename = require('history').useBasename;

var history = useBasename(createHistory)({
  basename: '/transitions'
});

var Dz = React.createClass({
  getInitialState: function() {
    return {files: []}
  },

  componentDidMount: function(){
    this.setState({files: this.state.files})
  },

  onDrop: function(files) {
    this.setState({files: files})
  },

  render: function() {
    var dzStyle = {
      textAlign: "center",
      fontSize: 20,
      width: 200,
      height: 150,
      borderWidth: 2,
      borderColor: '#003d7c',
      borderStyle: 'dashed',
      borderRadius: 5,
      margin: "auto",
      padding: "10px",
      color: "white"
    };

    var parentStyle = {
      color: "white"
    };

    return (
      <div>
  	    <Dropzone onDrop={this.onDrop} style={dzStyle}>
          <div>Simply drop or click to attach your Job Description and Resumes here.</div>
        </Dropzone>
        
        {this.state.files.length > 0 ? 
        <div style={parentStyle}>
          <h2>{this.state.files.length} file(s):</h2>
          <div>{this.state.files.map((file) => <p key={file.name}>{file.name}</p> )}</div>
          <br />
          <UploadFiles files={this.state.files} />
        </div>
        : null}
      </div>
    )
  }
});

var UploadFiles = React.createClass({
  mixins: [ History ],

  onUpload: function(e) {
    e.preventDefault();
    console.log(this.props.files);
    var files = this.props.files;

    this.history.pushState(null, 'results');
    
    var req = superagent.post('http://localhost:5000/upload');
    files.forEach((file)=> {
        req.attach("files", file, file.name);
    });
    req.end(function(err, res){
      console.log("error posting resumes", err);
      console.log("success posting resumes", res);
    });
  },

  render: function() {
    var uploadBtnStyle = {
      color: "white",
      fontSize: 20,
      borderRadius: 5,
      borderColor: "#003d7c",
      background: "#003d7c",
      cursor: "pointer"
    };

    return (
      <form onSubmit={this.onUpload}>
        <input type="submit" value="Upload Files" style={uploadBtnStyle}/>
      </form>
    )
  }
});

var UploadBox = React.createClass({
  render: function() {
    var parentStyle = {
      textAlign: "center",
      fontFamily: "HelveticaNeue-Light"
    };

    var titleStyle = {
      color: "white",
      background: "#003d7c",
      fontSize: 50
    };

    return (
      <div style={parentStyle}>
        <div style={titleStyle}>CS3219 Project - CViA</div>
        <br />
        <Dz />
      </div>
    );
  }
});

var Results = React.createClass({
  getInitialState: function() {
    return {data: []};
  },

  componentDidMount: function() {
    // loading results from server for initialization
    this.loadResultsFromServer();
  },

  loadResultsFromServer: function() {
    superagent
    .get('http://localhost:5000/analyzer')
    .end(function(err, res){
      if (res) {
        this.setState({data: JSON.parse(res.text)});
      } else {
        console.log("error loading results from server: ", err);
      }
    }.bind(this));
  },

  render: function() {
    var titleStyle = {
      color: "white",
      background: "#003d7c",
      fontSize: 50,
      textAlign: "center",
      fontFamily: "HelveticaNeue-Light"
    };

    return (
      <div>
        <div style={titleStyle}>Results</div>
        <ResultList data={this.state.data} />
      </div>
    );
  }
});

var ResultList = React.createClass({
  render: function() {
    var tableStyle = {
      margin: "auto",
      padding: 50,
      fontFamily: "HelveticaNeue-Light",
      fontSize: 20,
      color: "white"
    };

    var headStyle = {
      color: "#003d7c"
    };

    var resultNodes = this.props.data.map(function (result) {
      return (
        <Result name={result.Name}>
          {result.Score}
        </Result>
      );
    });
    
    return (
      <div>
        <table style={tableStyle}>
          <thead style={headStyle}>
            <th>Name | Score</th>
          </thead>
          <tbody>
              {resultNodes}
          </tbody>
        </table>
      </div>
    );
  }
});

var Result = React.createClass({
  render: function() {
    var scoreStyle = {
      display: "inline-block",
      right: 0
    };

    // the marked library will take Markdown text and convert to raw HTML, sanitize: true tells marked to escape any HTML mark up instead of passing it through unchanged.
    var rawMarkup = marked(this.props.children.toString(), {sanitize: true});

    return (
      <div>
        {this.props.name} - <span style={scoreStyle} dangerouslySetInnerHTML={{__html: rawMarkup}} />
      </div>
    );
  }
});

React.render(
  (
    <Router>
      <Route path="/" component={UploadBox} />
      <Route path="results" component={Results} />
    </Router>
  )
  , document.getElementById('app')
);
