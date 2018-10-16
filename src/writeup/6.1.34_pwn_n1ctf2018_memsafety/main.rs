#![allow(unused_variables, unused_imports, non_snake_case, dead_code, unused_assignments)]

use std::io::{stdin, stdout, BufReader, Error, Stdin};
use std::str::{FromStr, from_utf8};
use std::fmt::{Debug};
use std::io::prelude::*;
use std::process;
use std::convert::AsRef;
use std::cmp::*;
use std::collections::HashMap;

pub struct StdReader<T: Read> {
    reader: BufReader<T>,
}

impl<T: Read> StdReader<T> {
    pub fn new(stream: T) -> StdReader<T> {
        StdReader { reader: BufReader::new(stream) }
    }

    pub fn get<U: FromStr>(&mut self) -> Result<U, Error>
        where <U as FromStr>::Err: Debug, {
        let mut s = String::new();
        let result = self.reader.read_line(&mut s);
        match result {
            Ok(x) => Ok(s.trim().parse().unwrap()),
            Err(err) => Err(err.into())
        }
    }

    pub fn gets<U: FromStr>(&mut self) -> Result<Vec<U>, Error>
        where <U as FromStr>::Err: Debug, {
        let mut s = String::new();
        let result = self.reader.read_line(&mut s);
        match result {
            Ok(x) => Ok(s.trim().split_whitespace().map(|x| { x.parse().unwrap() }).collect()),
            Err(err) => Err(err.into())
        }
    }

    pub fn getline(&mut self) -> Result<String, Error> {
        let mut s = String::new();
        let result = self.reader.read_line(&mut s);
        match result {
            Ok(x) => Ok(String::from(s.trim())),
            Err(err) => Err(err.into())
        }
    }
}

#[derive(Debug, Clone)]
pub enum TokenTypes {
    Null,
    Int(i32),
    Str(String),
    Vector(Vec<i32>),
    Operator(u8),
    Parenthesis(u8),
}

#[derive(Debug, Clone)]
pub struct Token {
    val: TokenTypes
}

impl Token {
    pub fn new(val: TokenTypes) -> Token {
        Token { val : val }
    }

    pub fn token_type(&self) -> i32 {
        match self.val {
            TokenTypes::Null => 0,
            TokenTypes::Int(x) => 1,
            TokenTypes::Str(ref s) => 2,
            TokenTypes::Vector(ref v) => 3,
            TokenTypes::Operator(c) => 4,
            TokenTypes::Parenthesis(p) => 5,
        }
    }

    pub fn precedence(&self) -> i32 {
        if self.token_type() != 4 {
            panic!("precedence() called on non-operator token");
        }

        if let TokenTypes::Operator(o) = self.val {
            return match o {
                43 | 45 => 0,
                42 | 47 => 1,
                _ => unreachable!(),
            };
        }
        unreachable!();
    }

    pub fn is_leftparen(&self) -> bool {
        if self.token_type() == 5 {
            if let TokenTypes::Parenthesis(p) = self.val {
                if p == 40 {
                    return true;
                }
            }
        }
        false
    }

    pub fn is_operand(&self) -> bool {
        if self.token_type() >= 1 && self.token_type() <= 3 {
            return true;
        }
        false
    }

    pub fn unwrap_int(&self) -> Option<i32> {
        if self.token_type() != 1 {
            return None;
        }
        if let TokenTypes::Int(e) = self.val {
            return Some(e);
        }
        unreachable!();
    }

    pub fn unwrap_string(&self) -> Option<String> {
        if self.token_type() != 2 {
            return None;
        }
        if let TokenTypes::Str(ref s) = self.val {
            return Some(s.clone());
        }
        unreachable!();
    }

    pub fn unwrap_vec(&self) -> Option<Vec<i32>> {
        if self.token_type() != 3 {
            return None;
        }
        if let TokenTypes::Vector(ref v) = self.val {
            return Some(v.clone());
        }
        unreachable!();
    }
}

impl PartialEq for Token {
    fn eq(&self, other: &Token) -> bool {
        if self.token_type() == other.token_type() {
            return match self.val {
                TokenTypes::Null => true,
                TokenTypes::Int(x1) => {
                    let x2 = match other.val { 
                        TokenTypes::Int(x) => x, 
                        _ => unreachable!()
                    };
                    x1 == x2
                },
                TokenTypes::Str(ref s1) => {
                    let s2 = match other.val {
                        TokenTypes::Str(ref s) => s,
                        _ => unreachable!()
                    };
                    s1 == s2
                }
                TokenTypes::Vector(ref v1) => {
                    let v2 = match other.val {
                        TokenTypes::Vector(ref v) => v,
                        _ => unreachable!()
                    };
                    v1 == v2
                },
                TokenTypes::Operator(o1) => {
                    let o2 = match other.val {
                        TokenTypes::Operator(o) => o,
                        _ => unreachable!()
                    };
                    o1 == o2
                },
                _ => false
            }
        }
        false
    }
}
impl Eq for Token { }

impl PartialOrd for Token {
    fn partial_cmp(&self, other: &Token) -> Option<Ordering> {
        if self.token_type() != other.token_type() {
            return None;
        }

        match self.val { 
            TokenTypes::Null => Some(Ordering::Equal),
            TokenTypes::Int(x1) => {
                Some(x1.cmp(match other.val {
                    TokenTypes::Int(ref x2) => x2,
                    _ => unreachable!()
                }))
            },
            TokenTypes::Str(ref s1) => {
                Some(s1.cmp(match other.val {
                    TokenTypes::Str(ref s2) => s2,
                    _ => unreachable!()
                }))
            },
            TokenTypes::Vector(ref v1) => {
                Some(v1.cmp(match other.val {
                    TokenTypes::Vector(ref v2) => v2,
                    _ => unreachable!()
                }))
            },
            TokenTypes::Operator(o1) => {
                Some(self.precedence().cmp(&other.precedence()))
            },
            _ => None
        }
    }
}

#[derive(Debug)]
pub struct Lexer {
    input: String,
    idx: usize
}

impl Lexer {
    pub fn new(input: String) -> Lexer {
        Lexer { input: input, idx: 0 }
    }

    pub fn next_token(&mut self) -> Result<Token, String> {
        self.skip_whitespace();

        if let Ok(chr) = self.next_char() {
            let result = match chr {
                43 | 45 | 42 | 47 => { self.idx += 1; Ok(Token::new(TokenTypes::Operator(chr))) },
                41 | 40 => { self.idx += 1; Ok(Token::new(TokenTypes::Parenthesis(chr))) },
                91 => {
                    match self.next_vector() {
                        Ok(x) => { self.idx += 1; Ok(Token::new(TokenTypes::Vector(x))) },
                        Err(s) => Err(s)
                    }
                },
                34 => {
                    match self.next_string() {
                        Ok(x) => { self.idx += 1; Ok(Token::new(TokenTypes::Str(x))) },
                        Err(s) => Err(s)
                    }
                },
                48 ... 57 => {
                    match self.next_int() {
                        Ok(x) => Ok(Token::new(TokenTypes::Int(x))),
                        Err(s) => Err(s)
                    }
                },
                _ => Err(String::from("Invalid token"))
            };
            return result;
        }
        Err(String::from("EOL"))
    }

    fn next_char(&mut self) -> Result<u8, String> {
        let slice = self.input.as_bytes();
        let length = self.input.len();
        
        if self.idx >= length {
            return Err(String::from("EOL"));
        }
        Ok(slice[self.idx])
    }

    fn skip_whitespace(&mut self) {
        let slice = self.input.as_bytes();
        while self.idx < self.input.len() && slice[self.idx] == 0x20 {
            self.idx += 1;
        }
    }

    fn next_int(&mut self) -> Result<i32, String> {
        self.skip_whitespace();
        
        let slice = self.input.as_bytes();
        let length = self.input.len();
        let curidx = self.idx;
        let mut result: i32 = 0;
        loop {
            if self.idx < length && slice[self.idx] >= 0x30 && slice[self.idx] <= 0x39 {
                result = result * 10 + (slice[self.idx] as i32 - 0x30);
                self.idx += 1;
            } else {
                break;
            }
        }
        Ok(result)
    }

    fn next_string(&mut self) -> Result<String, String> {
        self.skip_whitespace();
        
        let slice = self.input.as_bytes();
        let length = self.input.len();
        let curidx = self.idx;

        self.idx += 1;
        loop {
            if self.idx < length && slice[self.idx] != 34 {
                self.idx += 1;
            } else {
                break;
            }
        }

        if self.idx >= length || slice[self.idx] != 34 {
            Err(String::from("Terminator not found"))
        } else {
            let bytes = &slice[curidx+1..self.idx];
            if let Ok(v) = from_utf8(bytes) {
                Ok(String::from(v))
            } else {
                Err(String::from("Invalid UTF-8 Sequence"))
            }
        }
    }

    fn next_vector(&mut self) -> Result<Vec<i32>, String> {
        let mut result: Vec<i32> = Vec::new();

        loop {
            self.idx += 1;
            
            self.skip_whitespace();
            if let Ok(chr) = self.next_char() {
                if chr < 48 && chr > 57 {
                    return Err(String::from("Invalid syntax"));
                }
                match self.next_int() {
                    Ok(x) => { result.push(x); },
                    Err(s) => { return Err(s); }
                }
            } else {
                return Err(String::from("EOL"));
            }

            self.skip_whitespace();
            if let Ok(chr) = self.next_char() {
                if chr == 93 {
                    return Ok(result);
                } else if chr != 44 {
                    return Err(String::from("Invalid terminator"));
                }
            } else {
                return Err(String::from("EOL"));
            }
        }
    }
}

#[derive(Debug)]
pub struct Parser {
    evalstk: Vec<Token>,
    tempstk: Vec<Token>,
    lexer: Lexer,
}

impl Parser {
    pub fn new(expr: String) -> Parser {
        Parser {
            lexer : Lexer::new(expr),
            evalstk : Vec::new(),
            tempstk : Vec::new(),
        }
    }

    fn peek_last(&mut self) -> Option<Token> {
        if self.tempstk.len() == 0 {
            return None;
        }
        Some(self.tempstk[self.tempstk.len() - 1].clone())
    }

    fn parse(&mut self) -> Result<u8, String> {
        loop {
            let token = self.lexer.next_token();
            match token {
                Ok(tk) => {
                    match tk.token_type() {
                        1 ... 3 => {
                            self.evalstk.push(tk);
                        },
                        4 => {
                            while let Some(ltk) = self.peek_last() {
                                if ltk.is_leftparen() {
                                    break;
                                }

                                if tk.precedence() <= ltk.precedence() {
                                    self.evalstk.push(self.tempstk.pop().unwrap());
                                } else {
                                    break;
                                }
                            }
                            self.tempstk.push(tk);
                        }
                        5 => {
                            if tk.is_leftparen() {
                                self.tempstk.push(tk);
                            } else {
                                let mut found_leftparen = false;
                                while let Some(lp) = self.tempstk.pop() {
                                    if lp.is_leftparen() {
                                        found_leftparen = true;
                                        break;
                                    } else {
                                        self.evalstk.push(lp);
                                    }
                                }
                                if !found_leftparen {
                                    return Err(String::from("Missing left parenthesis"));
                                }
                            }
                        }
                        _ => unreachable!(),
                    };
                },
                Err(e) => {
                    if e == "EOL" {
                        break;
                    } else {
                        return Err(e);
                    }
                },
            };
        }

        while !self.tempstk.is_empty() {
            self.evalstk.push(self.tempstk.pop().unwrap());
        }
        Ok(0)
    }

    fn eval_one(&mut self) -> Result<Token, String> {
        if self.evalstk.is_empty() {
            return Err(String::from("empty stack"));
        }
        
        let token = self.evalstk.pop().unwrap();
        if token.is_operand() {
            return Ok(token);
        }
        
        if let TokenTypes::Operator(op) = token.val {
            let right_oprnd = self.eval_one();
            if let Err(err) = right_oprnd {
                return Err(err);
            }
            let left_oprnd = self.eval_one();
            if let Err(err) = left_oprnd {
                return Err(err);
            }
            let lt = left_oprnd.unwrap();
            let rt = right_oprnd.unwrap();
            if lt.token_type() != rt.token_type() {
                return Err(String::from("Incompatible types of operands"));
            }

            return match op {
                43 => {
                    match lt.token_type() {
                        1 => {
                            Ok(Token::new(TokenTypes::Int(lt.unwrap_int().unwrap() + rt.unwrap_int().unwrap())))
                        },
                        2 => {
                            Ok(Token::new(TokenTypes::Str(lt.unwrap_string().unwrap() + &rt.unwrap_string().unwrap())))
                        },
                        3 => {
                            let mut lv = lt.unwrap_vec().unwrap();
                            lv.extend(&rt.unwrap_vec().unwrap());
                            Ok(Token::new(TokenTypes::Vector(lv)))
                        }
                        _ => unreachable!(),
                    }
                },
                45 => {
                    match lt.token_type() {
                        1 => {
                            Ok(Token::new(TokenTypes::Int(lt.unwrap_int().unwrap() - rt.unwrap_int().unwrap())))
                        },
                        2 => {
                            Err(String::from("String subtraction not supported"))
                        },
                        3 => {
                            Err(String::from("Vector subtraction not supported"))
                        },
                        _ => unreachable!()
                    }
                },
                42 => {
                    match lt.token_type() {
                        1 => {
                            Ok(Token::new(TokenTypes::Int(lt.unwrap_int().unwrap() * rt.unwrap_int().unwrap())))
                        },
                        2 => {
                            Err(String::from("String multiplication not supported"))
                        },
                        3 => {
                            Err(String::from("Vector multiplication not supported"))
                        },
                        _ => unreachable!()
                    }
                },
                47 => {
                    match lt.token_type() {
                        1 => {
                            Ok(Token::new(TokenTypes::Int(lt.unwrap_int().unwrap() / rt.unwrap_int().unwrap())))
                        },
                        2 => {
                            Err(String::from("String division not supported"))
                        },
                        3 => {
                            Err(String::from("Vector division not supported"))
                        },
                        _ => unreachable!()
                    }
                },
                _ => unreachable!(),
            }
        }
        unreachable!();
    }

    pub fn eval(&mut self) -> Result<Token, String> {
        if let Err(err) = self.parse() {
            return Err(err);
        }
        self.eval_one()
    }
}

#[derive(Debug)]
pub struct Globals {
    intvar: Vec<i32>,
    strvar: Vec<String>,
    vecvar: Vec<Vec<i32>>,
}

impl Globals {
    pub fn new() -> Globals {
        Globals {
            intvar: Vec::with_capacity(10),
            strvar: Vec::with_capacity(10),
            vecvar: Vec::with_capacity(10),
        }
    }

    pub fn addint(&mut self, v: i32) {
        self.intvar.push(v);
    }

    pub fn addstr(&mut self, v: &String) {
        self.strvar.push(v.clone());
    }

    pub fn addvec(&mut self, v: &Vec<i32>) {
        self.vecvar.push(v.clone());
    }

    pub fn getint(&self, idx: usize) -> i32 {
        self.intvar[idx]
    }

    pub fn getstr(&self, idx: usize) -> &String {
        &self.strvar[idx]
    }

    pub fn getvec(&self, idx: usize) -> &Vec<i32> {
        &self.vecvar[idx]
    }

    pub fn getvecint(&mut self, idx: usize, idy: usize) -> i32 {
        self.vecvar[idx][idy]
    }

    pub fn cloneint(&mut self, idx: usize) {
        let v = self.intvar[idx];
        self.intvar.push(v);
    }

    pub fn clonestr(&mut self, idx: usize) {
        let v = self.strvar[idx].clone();
        self.strvar.push(v);
    }

    pub fn clonevec(&mut self, idx: usize) {
        let v = self.vecvar[idx].clone();
        self.vecvar.push(v);
    }

    pub fn setint(&mut self, idx: usize, v: i32) {
        self.intvar[idx] = v;
    }

    pub fn setstr(&mut self, idx: usize, v: &String) {
        panic!("Strings are immutable.");
    }

    pub fn setvec(&mut self, idx: usize, idy: usize, v: i32) {
        self.vecvar[idx][idy] = v;
    }

    pub fn show(&self, v: &String) {
        let idx = String::from(&v.as_str()[5..v.len()]).parse::<usize>().unwrap();
        if v.starts_with("int: ") {
            println!("Result : {}", self.getint(idx));
        } else if v.starts_with("str: ") {
            println!("Result : {}", self.getstr(idx));
        } else if v.starts_with("vec: ") {
            println!("Result : {:?}", self.getvec(idx));
        } else {
            println!("Unknown variable!");
        }
        return;
    }
}

fn safe_flush() {
    if let Err(err) = stdout().flush() {
        println!("Internal error, contact admin! {}", err);
        process::exit(1);
    }
}

fn calculator(globals: &mut Globals) {
    println!("To use the calculator, type some expression.");
    
    let mut reader = StdReader::new(stdin());
    loop {
        print!(">>> "); safe_flush();
        if let Ok(expr) = reader.getline() {
            if expr == "exit" {
                println!("Bye!");
                break;
            }

            if expr == "check" {
                println!("Input the variable name you want to check after prompt.");
                loop {
                    print!(">>> "); safe_flush();
                    if let Ok(expr) = reader.getline() {
                        if expr == "done" {
                            break;
                        }
                        globals.show(&expr);
                    } else {
                        process::exit(1);
                    }
                }
                continue;
            }

            let mut parser = Parser::new(expr);
            let result = parser.eval();
            match result {
                Err(err) => println!("Error : {}", err),
                Ok(r) => {
                    match r.token_type() {
                        1 => {
                            let resint = r.unwrap_int();
                            if let None = resint {
                                println!("Internal error, contact admin");
                                process::exit(1);
                            }
                            
                            let mut k = resint.unwrap();
                            if k == 0x13337 {
                                let mut var = 0;
                                println!("1337 number!");
                                println!("Want to modify this number?");
                                println!("1. Increment");
                                println!("2. Decrement");
                                println!("3. Reset");
                                println!("4. var = number");
                                println!("5. number = var");
                                println!("6. Set var");
                                println!("7. number += var");
                                println!("8. number -= var");
                                println!("9. Set global vector number");
                                println!("0. Done!");
                                loop {
                                    print!("$ "); safe_flush();
                                    if let Ok(x) = reader.get::<i32>() {
                                        match x {
                                            1 => k = k + 1,
                                            2 => k = k - 1,
                                            3 => k = 0,
                                            4 => var = k,
                                            5 => k = var,
                                            6 => {
                                                if let Ok(o) = reader.get::<i32>() {
                                                    var = o;
                                                }
                                            },
                                            7 => k += var,
                                            8 => k -= var,
                                            9 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(idx) = reader.get::<usize>() {
                                                    print!("Index => "); safe_flush();
                                                    if let Ok(idy) = reader.get::<usize>() {
                                                        globals.setvec(idx, idy, k);
                                                    }
                                                }
                                            },
                                            0 => break,
                                            _ => println!("Unknown option."),
                                        };
                                    } else {
                                        process::exit(0);
                                    }
                                }
                            } else {
                                println!("normal number... ");
                                println!("Want to modify this number?");
                                println!("1. Leetify");
                                println!("2. Clone global integer");
                                println!("0. Done!");
                                loop {
                                    print!("$ "); safe_flush();
                                    if let Ok(x) = reader.get::<i32>() {
                                        match x {
                                            1 => k = 0x13337,
                                            2 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(input) = reader.get::<usize>() {
                                                    globals.cloneint(input);
                                                }
                                            },
                                            0 => break,
                                            _ => println!("Unknown option."),
                                        };
                                    } else {
                                        process::exit(0);
                                    }
                                }
                            }

                            print!("Store result? (y/n): "); safe_flush();
                            if let Ok(yesno) = reader.getline() {
                                if yesno == "y" {
                                    globals.addint(k);
                                }
                            } else {
                                println!("I/O Error");
                                process::exit(1);
                            }
                        },
                        2 => {
                            let resstr = r.unwrap_string();
                            let mut k = String::new();

                            if let None = resstr {
                                println!("Internal error, contact admin!");
                                process::exit(1);
                            }
                            else if resstr.unwrap().len() > 100 {
                                println!("Long string!");
                                println!("Want to modify this string?");
                                println!("1. Append");
                                println!("2. Prepend");
                                println!("3. Append from globals");
                                println!("4. Prepend from globals");
                                println!("5. Save current value to globals");
                                println!("6. Clone global string");
                                println!("0. Done!");
                                k = r.unwrap_string().unwrap();

                                loop {
                                    print!("$ "); safe_flush();
                                    if let Ok(x) = reader.get::<i32>() {
                                        match x {
                                            0 => break,
                                            1 | 2 => {
                                                print!("Input => "); safe_flush();
                                                if let Ok(input) = reader.getline() {
                                                    if x == 1 {
                                                        k = k + &input;
                                                    } else {
                                                        k = input + &k;
                                                    }
                                                }
                                            },
                                            3 | 4 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(input) = reader.get::<usize>() {
                                                    let var = globals.getstr(input);
                                                    if x == 3 {
                                                        k = k + var;
                                                    } else {
                                                        k = var.clone() + &k;
                                                    }
                                                }
                                            },
                                            5 => {
                                                globals.addstr(&k);
                                            },
                                            6 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(input) = reader.get::<usize>() {
                                                    globals.clonestr(input);
                                                }
                                            },
                                            _ => println!("Unknown option!"),
                                        };
                                    } else {
                                        process::exit(0);
                                    }
                                }
                            } else {
                                println!("Short string... ");
                                println!("Want to modify this string?");
                                println!("1. Double");
                                println!("2. Clone global string");
                                println!("0. Done!");
                                k = r.unwrap_string().unwrap();

                                loop {
                                    print!("$ "); safe_flush();
                                    if let Ok(x) = reader.get::<i32>() {
                                        match x {
                                            1 => k = k.clone() + &k,
                                            2 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(input) = reader.get::<usize>() {
                                                    globals.clonestr(input);
                                                }
                                            },
                                            0 => break,
                                            _ => println!("Unknown option!"),
                                        };
                                    } else {
                                        process::exit(0);
                                    }
                                }
                            }

                            print!("Store result? (y/n): "); safe_flush();
                            if let Ok(yesno) = reader.getline() {
                                if yesno == "y" {
                                    globals.addstr(&k);
                                }
                            } else {
                                println!("I/O Error");
                                process::exit(1);
                            } 
                        },
                        3 => {
                            let resvec = r.unwrap_vec();
                            let mut result: Vec<i32> = vec![];

                            if let None = resvec {
                                println!("Internal error, contact admin.");
                                process::exit(1);
                            } else if resvec.unwrap().len() <= 100 {
                                println!("Small vector...");
                                println!("Want to modify this vector?");
                                println!("1. Append number");
                                println!("2. Prepend number");
                                println!("3. Show number");
                                println!("4. Save current value to globals");
                                println!("5. Clone global vector");
                                println!("6. Set number");
                                println!("0. Done!");

                                let mut k = r.unwrap_vec().unwrap();
                                loop {
                                    print!("$ "); safe_flush();
                                    if let Ok(x) = reader.get::<i32>() {
                                        match x {
                                            1 => {
                                                print!("Enter the number: "); safe_flush();
                                                if let Ok(num) = reader.get::<i32>() {
                                                    k.push(num);
                                                }
                                            },
                                            2 => {
                                                print!("Enter the number: "); safe_flush();
                                                if let Ok(num) = reader.get::<i32>() {
                                                    k.insert(0, num);
                                                }
                                            },
                                            3 => {
                                                print!("Enter the number: "); safe_flush();
                                                if let Ok(num) = reader.get::<usize>() {
                                                    if num >= k.len() {
                                                        println!("Invalid index.");
                                                    } else {
                                                        println!("Result: {}", k[num]);
                                                    }
                                                }
                                            },
                                            4 => {
                                                globals.addvec(&k);
                                            },
                                            5 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(num) = reader.get::<usize>() {
                                                    globals.clonevec(num);
                                                }
                                            },
                                            6 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(num) = reader.get::<usize>() {
                                                    print!("Value => "); safe_flush();
                                                    if let Ok(value) = reader.get::<i32>() {
                                                        k[num] = value;
                                                    }
                                                }
                                            },
                                            0 => break,
                                            _ => println!("Unknown option!"),
                                        };
                                    } else {
                                        process::exit(0);
                                    }
                                    result = k.clone();
                                }
                            } else {
                                println!("Large vector...");
                                println!("Want to modify this vector?");
                                println!("1. Append number");
                                println!("2. Prepend number");
                                println!("3. Append number from globals");
                                println!("4. Prepend number from globals");
                                println!("5. Save current to globals");
                                println!("6. Show number");
                                println!("7. Set number");
                                println!("8. Clone global vector");
                                println!("9. Set number from global vector");
                                println!("0. Done!");

                                let mut k = resvec.unwrap();
                                loop {
                                    print!("$ "); safe_flush();
                                    if let Ok(x) = reader.get::<i32>() {
                                        match x {
                                            1 => {
                                                print!("Enter the number: "); safe_flush();
                                                if let Ok(num) = reader.get::<i32>() {
                                                    k.push(num);
                                                }
                                            },
                                            2 => {
                                                print!("Enter the number: "); safe_flush();
                                                if let Ok(num) = reader.get::<i32>() {
                                                    k.insert(0, num);
                                                }
                                            },
                                            3 | 4 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(varname) = reader.get::<usize>() {
                                                    let v = globals.getint(varname);
                                                    if x == 3 {
                                                        k.push(v);
                                                    } else if x == 4 {
                                                        k.insert(0, v);
                                                    }
                                                }
                                            },
                                            5 => {
                                                globals.addvec(&k);
                                            },
                                            6 => {
                                                print!("Enter the number: "); safe_flush();
                                                if let Ok(num) = reader.get::<usize>() {
                                                    if num >= k.len() {
                                                        println!("Invalid index.");
                                                    } else {
                                                        println!("Result: {}", k[num]);
                                                    }
                                                }
                                            },
                                            7 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(num) = reader.get::<usize>() {
                                                    print!("Value => "); safe_flush();
                                                    if let Ok(value) = reader.get::<i32>() {
                                                        k[num] = value;
                                                    }
                                                }
                                            },
                                            8 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(num) = reader.get::<usize>() {
                                                    globals.clonevec(num);
                                                }
                                            },
                                            9 => {
                                                print!("Index => "); safe_flush();
                                                if let Ok(idx) = reader.get::<usize>() {
                                                    print!("Index => "); safe_flush();
                                                    if let Ok(idy) = reader.get::<usize>() {
                                                        print!("Index => "); safe_flush();
                                                        if let Ok(idz) = reader.get::<usize>() {
                                                            k[idz] = globals.getvecint(idx, idy);
                                                        }
                                                    }
                                                }
                                            },
                                            1337 => {
                                                println!("{:?}", k);
                                            },
                                            0 => break,
                                            _ => println!("Unknown option!"),
                                        };
                                    } else {
                                        process::exit(0);
                                    }
                                    result = k.clone();
                                }
                            }
                            print!("Store result? (y/n): "); safe_flush();
                            if let Ok(yesno) = reader.getline() {
                                if yesno == "y" {
                                    globals.addvec(&result);
                                }
                            } else {
                                println!("I/O Error");
                                process::exit(1);
                            }
                        },
                        _ => unreachable!(),
                    }
                }
            };

        } else {
            println!("I/O Error");
            process::exit(1);
        }
    }
}

fn main() {
    println!("******** Welcome to Nu1L's Calc ********");
    let mut globals = Globals::new();

    // let's rock 'n roll
    calculator(&mut globals);
}