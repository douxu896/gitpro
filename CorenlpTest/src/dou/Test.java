package dou;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Properties;
import java.util.Random;


import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.SentimentAnnotator;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations.TreeAnnotation;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.PropertiesUtils;

public class Test {

	public static void main(String[] args) {
		// TODO 自动生成的方法存根
		 Test test = new Test();
		//读取xml文件的文件夹路径
	      String infile="E:"+File.separator+"XMLExample";
	    //输出预处理后的数据的csv文件
		  String outfile ="D:"+File.separator+"CSV"+File.separator;
		  String kuozhan = ".csv";
	    // creates a StanfordCoreNLP object, with POS tagging, lemmatization, NER, parsing, and coreference resolution
        Properties props = new Properties(); 
        props.put("annotators", "tokenize, cleanxml, ssplit, pos, lemma, ner, parse, dcoref");  //cleanxml, sentiment,
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
          
        List<String> file =getListFiles(infile,"",true);
        Iterator<String> it = file.iterator();
        while(it.hasNext()){
           String filename = (String)it.next();
    	   String text = test.Context(filename);
    	   Annotation document = new Annotation(text);
    	   pipeline.annotate(document);
    	   List<CoreMap> sentences = document.get(SentencesAnnotation.class);
    	   List<String> dataList=new ArrayList<String>();
    	   for(CoreMap sentence: sentences) {
    	           for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
    	        	   String word = token.get(TextAnnotation.class);
                       String pos = token.get(PartOfSpeechAnnotation.class);
                       dataList.add(word+","+pos);
    	           } 
            }
    	   System.out.println(filename);
    	   //filename.replaceFirst("E:\\XMLExample\\",""); 
    	   String name = filename.replaceFirst("E:\\\\XMLExample\\\\",""); 
    	   String name1 = name.replaceFirst(".xml",""); 
    	   //filename.replaceFirst("E",""); 
    	   System.out.println(name1);
    	   String subfile =outfile+File.separator+name1+kuozhan;
    	   System.out.println(subfile);
    	   CSVUtils.exportCsv(new File(subfile), dataList); //导出csv文件
    	         //    test.importCsv();  //导入csv文件
       }
     //   String text = test.Context("E:"+File.separator+"XMLExample"+File.separator+"AccessResourceExample2.xml");
       // String text = "Add your text here";
        // create an empty Annotation just with the given text
     /*   Annotation document = new Annotation(text);
      // run all Annotators on this text
        pipeline.annotate(document);
         // these are all the sentences in this document
         // a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
         List<CoreMap> sentences = document.get(SentencesAnnotation.class);
         File outfile = new File("D:"+File.separator+"q.csv");
         List<String> dataList=new ArrayList<String>();
         for(CoreMap sentence: sentences) {

           // traversing the words in the current sentence

           // a CoreLabel is a CoreMap with additional token-specific methods

           for (CoreLabel token: sentence.get(TokensAnnotation.class)) {

             // this is the text of the token

             String word = token.get(TextAnnotation.class);

             // this is the POS tag of the token

             String pos = token.get(PartOfSpeechAnnotation.class);

          //   System.out.println(word+" "+pos);
             dataList.add(word+","+pos);

           }*/
        //   CSVUtils.exportCsv(outfile, dataList); //导出csv文件
           // this is the parse tree of the current sentence
      //    test.importCsv();  //导入csv文件
         /*  Tree tree = sentence.get(TreeAnnotation.class);
           // this is the Stanford dependency graph of the current sentence

           SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);*/

         }
         // This is the coreference link graph

         // Each chain stores a set of mentions that link to each other,

         // along with a method for getting the most representative mention

         // Both sentence and token offsets start at 1!
       /*  Map<Integer, CorefChain> graph =

                 document.get(CorefChainAnnotation.class);*/

  //从XMl文件中读取
	String Context(String path) {
		// TODO 自动生成的方法存根
		 StringBuilder result = new StringBuilder();
	        try{
	            BufferedReader br = new BufferedReader(new FileReader(path));//构造一个BufferedReader类来读取文件
	            String s = null;
	            while((s = br.readLine())!=null){//使用readLine方法，一次读一行
	                result.append(System.lineSeparator()+s);
	            }
	            br.close();    
	        }catch(Exception e){
	            e.printStackTrace();
	        }
		return result.toString();
	}
	 //csv文件
    public void importCsv()  {
        List<String> dataList=CSVUtils.importCsv(new File("D:"+File.separator+"q.csv"));
        if(dataList!=null && !dataList.isEmpty()){
            for(String data : dataList){
                System.out.println(data);
            }
        }
    }
    public static List<String> getListFiles(String path, String suffix, boolean isdepth) {  
    	  List<String> lstFileNames = new ArrayList<String>();  
    	  File file = new File(path);  
    	  return listFile(lstFileNames, file, suffix, isdepth);  
    	 }  
    //显示目录的方法
    private static List<String> listFile(List<String> lstFileNames, File f, String suffix, boolean isdepth) {  
    	  // 若是目录, 采用递归的方法遍历子目录     
    	  if (f.isDirectory()) {  
    	   File[] t = f.listFiles();  
    	     
    	   for (int i = 0; i < t.length; i++) {  
    	    if (isdepth || t[i].isFile()) {  
    	     listFile(lstFileNames, t[i], suffix, isdepth);  
    	    }  
    	   }     
    	  } else {  
    	   String filePath = f.getAbsolutePath();     
    	   if (!suffix.equals("")) {  
    	    int begIndex = filePath.lastIndexOf("."); // 最后一个.(即后缀名前面的.)的索引   
    	    String tempsuffix = "";  
    	  
    	    if (begIndex != -1) {  
    	     tempsuffix = filePath.substring(begIndex + 1, filePath.length());  
    	     if (tempsuffix.equals(suffix)) {  
    	      lstFileNames.add(filePath);  
    	     }  
    	    }  
    	   } else {  
    	    lstFileNames.add(filePath);  
    	   }  
    	  }  
    	  return lstFileNames;  
    	 }  
	}

