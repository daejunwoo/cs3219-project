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

var UploadForm = React.createClass({
  getInitialState: function() {
    return {
      files: [],
      jobTitle: "",
      skills: "",
      more: ""
    }
  },

  componentDidMount: function(){
    this.setState({files: this.state.files});
  },

  handleChange1: function(e) {
    this.setState({jobTitle: e.target.value});
  },

  handleChange2: function(e) {
    this.setState({skills: e.target.value});
  },

  handleChange3: function(e) {
    this.setState({more: e.target.value});
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
      //margin: "auto",
      float: "right",
      padding: "10px",
      color: "white"
    };

    var parentStyle = {
      color: "white"
    };

    var fieldsStyle = {
      float: "left"
    };

    var formStyle = {
      padding: "100px",
      width: "50vw",
      margin: "auto"
    };

    return (
      <div style={formStyle}>
        <div style={fieldsStyle}>
          Job Title:<br /><input type="text" value={this.state.jobTitle} placeholder="Who?" onChange={this.handleChange1} />
          <br /><br />
          Skills:<br /><textarea type="text" value={this.state.skills} placeholder="What?" onChange={this.handleChange2} />
          <br /><br />
          Others:<br /><textarea type="text" value={this.state.more} placeholder="Anything else?" onChange={this.handleChange3} />
        </div>

        <Dropzone onDrop={this.onDrop} style={dzStyle}>
          <div>Simply drop or click to attach the Resumes here.</div>
        </Dropzone>

        {this.state.files.length > 0 ? 
        <div style={parentStyle}>
          <h2>{this.state.files.length} file(s):</h2>
          <div>{this.state.files.map((file) => <p key={file.name}>{file.name}</p> )}</div>
          <br />
          <UploadFiles files={this.state.files} jobTitle={this.state.jobTitle} skills={this.state.skills} more={this.state.more} />
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

    req.field("title", this.props.jobTitle);
    req.field("skills", this.props.skills);
    req.field("more", this.props.more);

    files.forEach((file)=> {
        req.attach("files", file, file.name);
    });

    req.end(function(err, res){
      if (res) {
        console.log("res", res);
        //this.history.pushState(null, 'results');
      } else {
        console.log("err", err);
      }
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
        <UploadForm />
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
        console.log(res);
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
      fontFamily: "HelveticaNeue-Light",
      textAlign: "center"
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
      var conStyle = {
        textAlign: "center"
      };

      var titleStyle = {
        fontSize: 30,
        color: "#003d7c",
        fontFamily: "HelveticaNeue-Light"
      };

      var resultNodes = this.props.data.map(function (result) {
        return (
          <Result name={result.Name}>
            {result.Score}
          </Result>
          );
      });

      return (
        <div style={conStyle}>
          <div style={titleStyle}>Name | Score</div>
          {resultNodes}
        </div>
      );
    }
  });

var Result = React.createClass({
    render: function() {
      var rankStyle = {
        color: "white",
        fontFamily: "HelveticaNeue-Light",
        fontSize: 20
      };

      var scoreStyle  = {
        display: "inline-block"
      };

      // the marked library will take Markdown text and convert to raw HTML, sanitize: true tells marked to escape any HTML mark up instead of passing it through unchanged.
      var rawMarkup = marked(this.props.children.toString(), {sanitize: true});
      
      return (
        <div style={rankStyle}>
            {this.props.name} | <span style={scoreStyle} dangerouslySetInnerHTML={{__html: rawMarkup}} />
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