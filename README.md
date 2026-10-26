# CellForge

### Cellular Automata Engine

CellForge is a programmable engine for creating cellular automata. It uses CellScript, a custom language used to create cellular automata, which are written rule by rule.

---

# Syntax:

## Example:

states {  
Form1;  
form2;  
}

grid {  
\!form2 \= \!form1 if (\`form2@1 \<= 1 or \`form2@1 \> 3\) end;  
\!form1 \= \!form2 if (\`form2@1 \== 2 or \`form2@1 \== 3\) end;  
}

# Syntax:

**\$**  \- current tile  
**\!**  \- form/state name

\`  \- neighbor count of a given state  
     \- syntax: \`STATE@RADIUS

**@**  \- radius for neighbor queries

**\==, \!=, \>, \<, \>=, \<=** \- comparisons  
**and, or, not**          \- logic operators

**{, }** \- header blocks  
**;**   \- end of line  
**\=**   \- assignment: set current cell to a form

**\[, \]** \- coordinate access: \[y,x\]  
**\+, \-, \*, /, %, \*\*** \- math  
**if**  \- start of condition  
**end** \- end of condition