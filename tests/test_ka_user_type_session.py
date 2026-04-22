import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USER_TYPE = ROOT / "ka_user_type.js"


def _run_user_type(local_storage: dict[str, str], session_storage: dict[str, str] | None = None) -> dict:
    session_storage = session_storage or {}
    script = f"""
const fs = require('fs');
const vm = require('vm');

function makeStorage(seed) {{
  const store = {{ ...seed }};
  return {{
    getItem(key) {{ return Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null; }},
    setItem(key, value) {{ store[key] = String(value); }},
    removeItem(key) {{ delete store[key]; }},
    dump() {{ return store; }},
  }};
}}

function makeNode(requirement) {{
  const attrs = requirement ? {{ 'data-ka-requires': requirement }} : {{}};
  const style = {{
    removeProperty(name) {{ delete this[name]; }},
  }};
  return {{
    style,
    dataset: {{}},
    parentNode: {{ removeChild() {{}} }},
    setAttribute(name, value) {{
      attrs[name] = String(value);
      if (name === 'data-ka-gated') this.dataset.kaGated = String(value);
    }},
    getAttribute(name) {{
      return Object.prototype.hasOwnProperty.call(attrs, name) ? attrs[name] : null;
    }},
    removeAttribute(name) {{
      delete attrs[name];
      if (name === 'data-ka-gated') delete this.dataset.kaGated;
    }},
  }};
}}

const listeners = {{}};
const sessionStorage = makeStorage({json.dumps(session_storage)});
const localStorage = makeStorage({json.dumps(local_storage)});
const gatedElement = makeNode('160-student');
const body = makeNode(null);
body.firstChild = null;
body.dataset = {{}};
body.style = {{}};
body.insertBefore = function () {{}};
const document = {{
  readyState: 'loading',
  body,
  addEventListener(name, handler) {{ listeners['document:' + name] = handler; }},
  getElementById(id) {{ return id === 'ka-imp-banner' ? null : null; }},
  querySelectorAll(selector) {{
    if (selector === '[data-ka-requires]') return [gatedElement];
    return [];
  }},
  createElement() {{
    return makeNode(null);
  }},
}};

const windowObj = {{
  sessionStorage,
  localStorage,
  KA: {{}},
  addEventListener(name, handler) {{ listeners['window:' + name] = handler; }},
  removeEventListener() {{}},
}};
windowObj.window = windowObj;

const context = {{
  console,
  document,
  window: windowObj,
  location: {{ reload() {{}} }},
  getComputedStyle() {{ return {{ paddingTop: '0px' }}; }},
}};

vm.runInNewContext(fs.readFileSync({json.dumps(str(USER_TYPE))}, 'utf8'), context);
const domReady = listeners['document:DOMContentLoaded'];
if (domReady) domReady();

process.stdout.write(JSON.stringify({{
  userType: context.window.KA.userType.get(),
  canSeeStudent: context.window.KA.userType.canSee('160-student'),
  gatedDisplay: gatedElement.style.display || '',
  gatedMarker: gatedElement.dataset.kaGated || '',
  sessionStorage: sessionStorage.dump(),
  listeners: Object.keys(listeners).sort(),
}}));
"""
    completed = subprocess.run(
        ["node", "-e", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)


def test_user_type_promotes_student_local_storage_into_student_access():
    result = _run_user_type(
        {
            "ka_access_token": "token-123",
            "ka_current_user": json.dumps(
                {
                    "email": "student@example.com",
                    "role": "student",
                }
            ),
        }
    )

    assert result["userType"] == "160-student"
    assert result["canSeeStudent"] is True
    assert result["gatedDisplay"] == ""
    assert result["gatedMarker"] == ""
    assert result["sessionStorage"]["ka.160.authed"] == "yes"
    assert result["sessionStorage"]["ka.studentEmail"] == "student@example.com"


def test_user_type_clears_stale_student_session_when_local_auth_missing():
    result = _run_user_type(
        {},
        {
            "ka.userType": "160-student",
            "ka.160.authed": "yes",
            "ka.studentEmail": "stale@example.com",
        },
    )

    assert result["userType"] == "visitor"
    assert result["canSeeStudent"] is False
    assert result["gatedDisplay"] == "none"
    assert result["gatedMarker"] == "hidden"
    assert "ka.160.authed" not in result["sessionStorage"]
    assert "ka.studentEmail" not in result["sessionStorage"]
    assert "window:pageshow" in result["listeners"]
    assert "window:storage" in result["listeners"]


def test_user_type_refresh_restores_hidden_student_element_after_login():
    script = f"""
const fs = require('fs');
const vm = require('vm');

function makeStorage(seed) {{
  const store = {{ ...seed }};
  return {{
    getItem(key) {{ return Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null; }},
    setItem(key, value) {{ store[key] = String(value); }},
    removeItem(key) {{ delete store[key]; }},
  }};
}}

function makeNode(requirement) {{
  const attrs = requirement ? {{ 'data-ka-requires': requirement }} : {{}};
  const style = {{ removeProperty(name) {{ delete this[name]; }} }};
  return {{
    style,
    dataset: {{}},
    parentNode: {{ removeChild() {{}} }},
    setAttribute(name, value) {{
      attrs[name] = String(value);
      if (name === 'data-ka-gated') this.dataset.kaGated = String(value);
    }},
    getAttribute(name) {{
      return Object.prototype.hasOwnProperty.call(attrs, name) ? attrs[name] : null;
    }},
    removeAttribute(name) {{
      delete attrs[name];
      if (name === 'data-ka-gated') delete this.dataset.kaGated;
    }},
  }};
}}

const listeners = {{}};
const sessionStorage = makeStorage({{}});
const localStorage = makeStorage({{}});
const gatedElement = makeNode('160-student');
const body = makeNode(null);
body.firstChild = null;
body.dataset = {{}};
body.style = {{ removeProperty(name) {{ delete this[name]; }} }};
body.insertBefore = function () {{}};
const document = {{
  readyState: 'loading',
  body,
  addEventListener(name, handler) {{ listeners['document:' + name] = handler; }},
  getElementById() {{ return null; }},
  querySelectorAll(selector) {{ return selector === '[data-ka-requires]' ? [gatedElement] : []; }},
  createElement() {{ return makeNode(null); }},
}};
const windowObj = {{
  sessionStorage,
  localStorage,
  KA: {{}},
  addEventListener(name, handler) {{ listeners['window:' + name] = handler; }},
}};
windowObj.window = windowObj;
const context = {{
  console,
  document,
  window: windowObj,
  location: {{ reload() {{}} }},
  getComputedStyle() {{ return {{ paddingTop: '0px' }}; }},
}};

vm.runInNewContext(fs.readFileSync({json.dumps(str(USER_TYPE))}, 'utf8'), context);
listeners['document:DOMContentLoaded']();
localStorage.setItem('ka_access_token', 'token-123');
localStorage.setItem('ka_current_user', JSON.stringify({{ email: 'student@example.com', role: 'student' }}));
context.window.KA.userType.refresh();

process.stdout.write(JSON.stringify({{
  display: gatedElement.style.display || '',
  marker: gatedElement.dataset.kaGated || '',
  userType: context.window.KA.userType.get(),
}}));
"""
    completed = subprocess.run(
        ["node", "-e", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    result = json.loads(completed.stdout)
    assert result["display"] == ""
    assert result["marker"] == ""
    assert result["userType"] == "160-student"
