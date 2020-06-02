from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()
        
    def _add_tokens(self):
        # Parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        # Brackets
        self.lexer.add('OPEN_BRA', r'\[')
        self.lexer.add('CLOSE_BRA', r'\]')
        #Float
        self.lexer.add('FLOAT', r'-?\d*\.\d+')
        # Int
        self.lexer.add('INT', r'-?\d+')
        # Colon
        self.lexer.add('COLON', r'\:')
        # Semi Colon
        self.lexer.add('SEMI_COLON', r'\;')
        # Coma
        self.lexer.add('COMA', r'\,')
        # Extension
        self.lexer.add('ADD', r'\+')
        #Predictive methods
        self.lexer.add('METHOD', r'SARIMA|EXPSM')
        #CLUSTERING methods
        self.lexer.add('CLUSTERING', r'KMEANS|GAUSSIAN|AGGLOMERATIVE|SPECTRAL')
        # Boolean
        self.lexer.add('BOOLEAN', r'False|True')
        # Type a
        self.lexer.add('TYPE_A', r'add|mul|additive|multiplicative')       
        #Equal
        self.lexer.add('EQUAL', r'=')
        #VARNAME
        self.lexer.add('VAR', r'[a-z]+[a-zA-Z0-9]*')
        #Forecast
        self.lexer.add('FORECAST', r'FORECAST')
        #Predict Clusters
        self.lexer.add('PREDICTION', r'PREDICT2|PREDICT')
        #Statistics
        self.lexer.add('STATS', r'STATS')
        #Print
        self.lexer.add('PRINT', r'PRINT')
        #Plot
        self.lexer.add('PLOT', r'PLOT')
        #Plot compared
        self.lexer.add('C_PLOT', r'C_PLOT')
        #Sentence
        self.lexer.add('SENTENCE', r"'[^']*'")
        # Ignore comments
        self.lexer.ignore(r'\$[^$]*\$')
        # Ignore spaces
        self.lexer.ignore(r'\s+')
        # Ignore endlines
        self.lexer.ignore(r'\n')
        
        
    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
