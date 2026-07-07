import CodeMirror from "@uiw/react-codemirror";
import { json, jsonParseLinter } from "@codemirror/lang-json";
import { linter, lintGutter } from "@codemirror/lint";
import { githubLight } from "@uiw/codemirror-theme-github";

export type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue };

function JsonEditor({
  value,
  onChange,
}: {
  value: JsonValue;
  onChange: (v: JsonValue) => void;
}) {
  const textValue = JSON.stringify(value, null, 2);

  return (
    <CodeMirror
      value={textValue}
      onChange={(newValue) => {
        try {
          const parsed = JSON.parse(newValue) as JsonValue;
          onChange(parsed);
        } catch {
          // Ignore invalid partial JSON while typing
        }
      }}
      theme={githubLight}
      extensions={[json(), linter(jsonParseLinter()), lintGutter()]}
      height="240px"
    />
  );
}

export default JsonEditor;