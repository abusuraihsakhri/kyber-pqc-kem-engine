/* Browser-only smoke test for the static telemetry console. No DOM package required. */
"use strict";
const fs = require("fs");
const vm = require("vm");
const assert = require("assert");
const path = require("path");

const html = fs.readFileSync(path.join(__dirname, "..", "web", "index.html"), "utf8");
const match = html.match(/<script>([\s\S]*?)<\/script>/i);
assert(match, "expected a JavaScript block");
const listeners = {};
const elements = {};
for (const id of ["audit-form","output","error","count","alerts","download",
                  "task_id","target_id","primary_metric","secondary_metric",
                  "status_descriptor","is_critical"]) {
  elements[id] = {
    textContent: "", disabled: true, value: "",
    checked: false, addEventListener: (type, fn) => { listeners[id+":"+type] = fn; },
    reportValidity: () => true
  };
}
const document = {
  getElementById: id => elements[id],
  createElement: () => ({click() {}, set href(v) {}, set download(v) {}})
};
const URL = {createObjectURL: () => "blob:test", revokeObjectURL: () => {}};
vm.runInNewContext(match[1], {document, URL, Blob});
assert(listeners["audit-form:submit"], "form submit handler missing");
assert(listeners["download:click"], "export handler missing");
const values = {task_id:"TASK",target_id:"KEY",primary_metric:"20",
                secondary_metric:"5",status_descriptor:"NOMINAL"};
for (const [key,val] of Object.entries(values)) elements[key].value = val;
const submit = () => listeners["audit-form:submit"]({preventDefault() {}});
submit();
assert.equal(JSON.parse(elements.output.textContent).overall_urgency, "ROUTINE");
assert.equal(elements.count.textContent, "1");
assert.equal(elements.download.disabled, false);
elements.is_critical.checked = true;
submit();
const critical = JSON.parse(elements.output.textContent);
assert.equal(critical.overall_urgency, "CRITICAL_STAT_PANIC");
assert.equal(critical.total_alerts, 1);
assert(!("audit_hash" in critical), "browser cannot claim HMAC signing");
elements.is_critical.checked = false;
elements.primary_metric.value = "Infinity";
submit();
assert(elements.error.textContent.includes("finite"));
assert.equal(elements.count.textContent, "2");
listeners["download:click"]();
process.stdout.write("Browser UI smoke tests passed\n");
