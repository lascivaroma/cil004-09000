__all__ = ['chetc']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['Epigraph2Markup'])
@Js
def PyJsHoisted_Epigraph2Markup_(replacements, this, arguments, var=var):
    var = Scope({'arguments':arguments, 'this':this, 'replacements':replacements}, var)
    var.registers(['replacements'])
    @Js
    def PyJs_anonymous_1_(ignore, this, arguments, var=var):
        var = Scope({'arguments':arguments, 'ignore':ignore, 'this':this}, var)
        var.registers(['ignore'])
        if (var.get('ignore')==Js('true')):
            var.get(u"this").put('ignoreLB', var.get('true'))
        else:
            var.get(u"this").put('ignoreLB', Js(False))
    PyJs_anonymous_1_._set_name('anonymous')
    @Js
    def PyJs_anonymous_2_(this, arguments, var=var):
        var = Scope({'arguments':arguments, 'this':this}, var)
        var.registers(['unicodeLetters'])
        var.put('unicodeLetters', Js('[A-Za-zªµºÀ-ÖØ-öø-ƺƼ-ƿ Ǆ-ʭΆΈ-ҁҌ-Ֆա-ևႠ-ჅḀ-ᾼιῂ-ῌ ῐ-Ίῠ-Ῥῲ-ῼⁿℂℇℊ-ℓℕℙ-ℝℤΩ ℨK-ℭℯ-ℱℳℴℹﬀ-ﬗＡ-Ｚａ-ｚ]'))
        var.get(u"this").put('replacements', var.get('Array').create())
        var.put('lines', var.get(u"this").get('replacementStr').callprop('split', JsRegExp('/\\r?\\n/')))
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get('lines').get('length')):
            try:
                var.put('line', var.get('lines').get(var.get('i')))
                if ((var.get('line').callprop('charAt', Js(0.0))!=Js('#')) and var.get('line').callprop('match', JsRegExp('/^\\s*$/')).neg()):
                    if (var.get(u"this").get('ignoreLB') and var.get('line').callprop('match', JsRegExp('/^\\\\n/'))).neg():
                        var.put('repl', var.get('line').callprop('split', JsRegExp('/\\s+=\\s+/')))
                        if (var.get('repl').get('length')==Js(2.0)):
                            var.get('repl').put('0', var.get('repl').get('0').callprop('replace', JsRegExp('/\\\\w/g'), var.get('unicodeLetters')))
                            if (var.get('repl').get('1')==Js('null')):
                                var.get('repl').put('1', Js(''))
                            var.get(u"this").get('replacements').callprop('push', var.get('repl'))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    PyJs_anonymous_2_._set_name('anonymous')
    @Js
    def PyJs_anonymous_3_(txt, find, this, arguments, var=var):
        var = Scope({'find':find, 'txt':txt, 'arguments':arguments, 'this':this}, var)
        var.registers(['find', 'txt'])
        if (var.get('txt')==var.get('find')):
            var.put('result', var.get('txt').callprop('replace', JsRegExp('/\\s/g'), Js('')).get('length'))
        else:
            var.put('result', Js(0.0))
            var.put('compare', var.get('txt'))
            while (var.get('compare').callprop('indexOf', var.get('find'))>=Js(0.0)):
                (var.put('result',Js(var.get('result').to_number())+Js(1))-Js(1))
                var.put('compare', var.get('compare').callprop('substr', (var.get('compare').callprop('indexOf', var.get('find'))+var.get('find').get('length'))))
        return var.get('result')
    PyJs_anonymous_3_._set_name('anonymous')
    @Js
    def PyJs_anonymous_4_(text, this, arguments, var=var):
        var = Scope({'text':text, 'arguments':arguments, 'this':this}, var)
        var.registers(['text', 'repl', 'result', 'idPattern', 'replace', 'targPattern', 'g', 'len', 'pattern', 're'])
        var.put('result', var.get('text'))
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get(u"this").get('replacements').get('length')):
            try:
                var.put('repl', var.get(u"this").get('replacements').get(var.get('i')))
                var.put('replace', var.get('repl').get('1'))
                if var.get('replace').callprop('match', JsRegExp('/%g/')):
                    var.put('pattern', var.get('RegExp').create(var.get('repl').get('0')))
                    while var.put('matches', var.get('result').callprop('match', var.get('pattern'))):
                        var.put('g', Js(0.0))
                        var.put('len', Js(0.0))
                        var.put('re', JsRegExp('/%g(\\d)/'))
                        if var.put('captured', var.get('re').callprop('exec', var.get('replace'))):
                            var.put('g', var.get('captured').get('1'))
                            var.put('replace', var.get('replace').callprop('replace', JsRegExp('/%g\\d/g'), Js('')))
                            var.put('re', JsRegExp('/%len(\\d)/'))
                            if var.put('captured', var.get('re').callprop('exec', var.get('replace'))):
                                var.put('len', var.get('captured').get('1'))
                                var.put('replace', var.get('replace').callprop('replace', JsRegExp('/%len\\d/g'), var.get(u"this").callprop('count', var.get('matches').get(var.get('g')), var.get('matches').get(var.get('len')))))
                                var.put('result', var.get('result').callprop('replace', var.get('pattern'), var.get('replace')))
                        var.put('replace', var.get('repl').get('1'))
                else:
                    var.put('pattern', var.get('RegExp').create(var.get('repl').get('0'), Js('g')))
                    var.put('result', var.get('result').callprop('replace', var.get('pattern'), var.get('replace')))
                while var.put('ids', var.get('result').callprop('match', JsRegExp('/id="%mkID(\\d)"/'))):
                    if (var.get('parseFloat')(var.get(u"this").get('id'))<Js(9.0)):
                        var.get(u"this").put('id', (Js('0')+(var.get('parseFloat')(var.get(u"this").get('id'))+Js(1.0))))
                    else:
                        var.get(u"this").put('id', (Js('')+(var.get('parseFloat')(var.get(u"this").get('id'))+Js(1.0))))
                    var.get(u"this").put('id', (Js('gap')+var.get(u"this").get('id')))
                    var.put('idPattern', var.get('RegExp').create(((Js('(id=")%mkID')+var.get('ids').get('1'))+Js('(")'))))
                    var.put('result', var.get('result').callprop('replace', var.get('idPattern'), ((Js('$1')+var.get(u"this").get('id'))+Js('$2'))))
                    if var.get('replace').callprop('match', JsRegExp('/target="%mkID\\d"/')):
                        var.put('targPattern', var.get('RegExp').create(((Js('(target=")%mkID')+var.get('ids').get('1'))+Js('(")'))))
                        var.put('result', var.get('result').callprop('replace', var.get('targPattern'), ((Js('$1')+var.get(u"this").get('id'))+Js('$2'))))
                    var.get(u"this").put('id', var.get(u"this").get('id').callprop('substr', Js(3.0)))
                while var.put('lines', var.get('result').callprop('match', JsRegExp('/lb n="%mkID(\\d)"/'))):
                    var.get(u"this").put('lineNum', (Js('')+(var.get('parseFloat')(var.get(u"this").get('lineNum'))+Js(1.0))))
                    var.put('idPattern', var.get('RegExp').create(((Js('(lb n=")%mkID')+var.get('lines').get('1'))+Js('(")'))))
                    var.put('result', var.get('result').callprop('replace', var.get('idPattern'), ((Js('$1')+var.get(u"this").get('lineNum'))+Js('$2'))))
                    if var.get('replace').callprop('match', JsRegExp('/target="%mkID\\d"/')):
                        var.put('targPattern', var.get('RegExp').create(((Js('(target=")%mkID')+var.get('lines').get('1'))+Js('(")'))))
                        var.put('result', var.get('result').callprop('replace', var.get('targPattern'), ((Js('$1')+var.get(u"this").get('lineNum'))+Js('$2'))))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        return var.get('result')
    PyJs_anonymous_4_._set_name('anonymous')
    PyJs_Object_0_ = Js({'id':var.get('String').create(Js('00')),'lineNum':var.get('String').create(Js('01')),'replacementStr':var.get('replacements'),'ignoreLB':Js(False),'lineBreaks':PyJs_anonymous_1_,'init':PyJs_anonymous_2_,'count':PyJs_anonymous_3_,'convert':PyJs_anonymous_4_})
    return PyJs_Object_0_
PyJsHoisted_Epigraph2Markup_.func_name = 'Epigraph2Markup'
var.put('Epigraph2Markup', PyJsHoisted_Epigraph2Markup_)
pass
pass


# Add lib to the module scope
chetc = var.to_python()