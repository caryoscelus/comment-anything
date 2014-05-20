/*
 *  Copyright (C) 2014 caryoscelus
 *  
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *  
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *  
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

function loadURL (url, mime, callback) {
    requestURL('GET', url, false, mime, null, callback)
}

function requestURL (type, url, mime_in, mime, content, callback) {
    var xobj = new XMLHttpRequest()
    xobj.overrideMimeType(mime)
    xobj.open(type, url, true)
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4) {
            callback(xobj.response)
        }
    }
    if (mime_in) {
        xobj.setRequestHeader('Content-Type', mime_in)
    }
    xobj.send(content)
}

function getParentUrl() {
    var isInIframe = (parent !== window)
    var parentUrl = null
    
    if (isInIframe) {
        parentUrl = document.referrer
    }
    
    return parentUrl
}

function renderComment (c) {
    var comments_div = document.getElementById('comment_anything_msgs')
    var comment_div = document.createElement('div')
    comments_div.appendChild(comment_div)
    
    comment_div.innerHTML = '<h5>'+c.nick+'</h5>'+'<p>'+c.text+'</p>'
}

function getPath () {
    if (getParentUrl() == null) {
        return window.location.pathname
    } else {
        alert(getParentUrl())
        var parser = document.createElement('a')
        parser.href = getParentUrl()
        return parser.pathname
    }
}

function reloadComments (message) {
    var comments_div = document.getElementById('comment_anything_msgs')
    comments_div.innerHTML = ''
    var msg_p = document.createElement('p')
    msg_p.innerHTML = message
    comments_div.appendChild(msg_p)
    
    loadURL(rest_server+'get_comments/'+site_id+'/root'+getPath(), 'application/json', function (response) {
        json = JSON.parse(response)
        comments = json.comments
        for (var i = 0; i < comments.length; ++i) {
            renderComment(comments[i])
        }
        comments_div.removeChild(msg_p)
    })
}

function post () {
    var nick = document.getElementById('comment_anything_nick').value
    var text = document.getElementById('comment_anything_text').value
    requestURL(
        'POST',
        rest_server+'add_comment/'+site_id+'/root'+getPath(),
        'application/json',
        'application/json',
        JSON.stringify({
            "nick": nick,
            "text": text
        }),
        function (response) {
            json = JSON.parse(response)
            if (json.status == 'ok') {
                reloadComments('comment posted, reloading..')
            } else {
                reloadComments('comment post failed, reloading..')
            }
        }
    )
}

reloadComments('loading comments..')
