#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:set sw=2 sts=2 expandtab:
#
# MIT License Copyright(c) 2017 Hiroshi Shimamoto

from flask import Flask, request, jsonify, redirect, Response
import requests
import json

app = Flask(__name__, static_folder = '')

class Host:
  def __init__(self, name):
    self.name = name
    self.urlhost = '127.0.0.1:80'
    self.valid = False

  def dict(self):
    return {
      'name': self.name,
      'urlhost': self.urlhost,
      'valid': self.valid,
    }

  def update(self, data):
    if 'urlhost' in data:
      self.urlhost = data['urlhost']
    if 'valid' in data:
      self.valid = data['valid']

  def redirect(self, path, req):
    url = 'http://' + self.urlhost + '/' + path
    print(url)
    if req.method == 'GET':
      print('get')
      resp = requests.get(url, stream = True, headers = req.headers, params = req.args)
    elif req.method == 'POST':
      print('post')
      resp = requests.post(url, stream = True, headers = req.headers, data = req.data)
    def generate():
      for chunk in resp.iter_content(4096):
        yield chunk
    return Response(generate(), headers = dict(resp.headers))

hosts = {
  'default': Host('default')
}

@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def root(path = ''):
  print('default route')
  print(path)
  dirs = path.split('/')
  print(dirs[0])
  if dirs[0] != 'config':
    host = hosts['default']
    if host.valid:
      return host.redirect(path, request)
  return redirect('config')

@app.route('/config')
@app.route('/config/<path:path>')
def config(path = '/'):
  if path == '/':
    return app.send_static_file('config.html')
  return app.send_static_file(path)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
  ls = []
  for host in hosts.values():
    print(host)
    if host.urlhost != '':
      ls.append(host.dict())
  return jsonify(ls)

@app.route('/setting', methods=['GET', 'POST'])
@app.route('/setting/<host>', methods=['GET', 'POST'])
@app.route('/setting/<host>/<key>', methods=['GET', 'POST'])
def setting(host = 'default', key = ''):
  print('setting: ' + host)
  if not host in hosts:
    hosts[host] = Host(host)
  host = hosts[host]
  if key == '':
    if request.method == 'POST':
      print('update: ' + json.dumps(request.json))
      host.update(request.json)
  return jsonify({'name':host.name})

@app.route('/route/<host>', methods=['GET', 'POST'])
@app.route('/route/<host>/', methods=['GET', 'POST'])
@app.route('/route/<host>/<path:path>', methods=['GET', 'POST'])
def route(host, path = ''):
  print('route to ' + host)
  if host in hosts:
    host = hosts[host]
    if host.valid:
      return host.redirect(path, request)
  return redirect('config')

if __name__ == '__main__':
  print(app.url_map)
  app.run(host = '0.0.0.0', port = 8080)
