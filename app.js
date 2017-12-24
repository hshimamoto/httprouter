// vim:set sw=2 sts=2:
//
// MIT License Copyright(c) 2017 Hiroshi Shimamoto

var app = new Vue({
  el: '#app',
  data: {
    settings: [],
    name: '',
  },
  created() {
    this.load();
  },
  methods: {
    load() {
      axios.post('/settings').then(resp => {
	this.settings = resp.data;
      });
    },
    add() {
      name = this.name;
      if (name != '') {
	console.log(this.name);
	this.name = '';
	data = {'name':this.name, 'urlhost':'127.0.0.1', 'valid':false};
	axios.post('/setting/' + name, data).then(resp => {
	  this.load();
	});
      }
    },
    update(s) {
      console.log(s.name + ':' + s.update + " " + s.valid);
      axios.post('/setting/' + s.name, s).then(resp => {
	// nothing to do
      });
    },
  }
});
