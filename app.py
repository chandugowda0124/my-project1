from flask import Flask, request, jsonify, render_template
from ast_engine import create_rule, combine_rules, evaluate_rule
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('rules.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/create_rule', methods=['POST'])
def api_create_rule():
    rule_string = request.json.get('rule_string')
    ast = create_rule(rule_string)
    
    # Store AST in the database
    conn = get_db_connection()
    conn.execute('INSERT INTO rules (rule, ast_repr) VALUES (?, ?)', (rule_string, repr(ast)))
    conn.commit()
    conn.close()

    return jsonify({"ast": repr(ast)})


@app.route('/api/combine_rules', methods=['POST'])
def api_combine_rules():
    rules = request.json.get('rules')
    combined_ast = combine_rules(rules)

    return jsonify({"combined_ast": repr(combined_ast)})


@app.route('/api/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    ast_repr = request.json.get('ast')  # String representation of AST
    user_data = request.json.get('user_data')  # e.g., {"age": 35, "department": "Sales"}

    # Evaluate rule using the AST
    combined_ast = eval(ast_repr)  # Convert string back to AST object (unsafe, for simplicity here)
    result = evaluate_rule(combined_ast, user_data)

    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)
