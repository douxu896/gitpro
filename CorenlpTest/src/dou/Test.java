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
	      String infile=File.separator+"media"+File.separator+"emily"+File.separator+"06C4707CC4707033"+File.separator+"XMLExample";
	    //输出预处理后的数据的csv文件
		  String outfile =File.separator+"home"+File.separator+"emily"+File.separator+"Desktop"+File.separator+"CSV";
		  String kuozhan = ".csv";
		  createDir(outfile);
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
    	   String name = getfilename(filename);
    	   System.out.println(name);
    	   String subfile =outfile+File.separator+name+kuozhan;
    	   System.out.println(subfile);
    	   CSVUtils.exportCsv(new File(subfile), dataList); //导出csv文件
    	         //    test.importCsv();  //导入csv文件
       }
         /*  Tree tree = sentence.get(TreeAnnotation.class);
           // this is the Stanford dependency graph of the current sentence
         SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);
         Both sentence and token offsets start at 1!
         Map<Integer, CorefChain> graph =
                  document.get(CorefChainAnnotation.class);*/
         }
    
		private static boolean createDir(String file) {
		// TODO Auto-generated method stub
			File dir = new File(file);
			if (dir.exists()) {// 判断目录是否存在
				System.out.println("创建CSV目录失败，目标目录已存在！");
				return false;
			}
			if (!file.endsWith(File.separator)) {// 结尾是否以"/"结束
				file = file + File.separator;
			}
			if (dir.mkdirs()) {// 创建目标目录
				System.out.println("创建CSV目录成功！" + file);
				return true;
			} else {
				System.out.println("创建CSV目录失败！");
				return false;
			}
	}

		private static String getfilename(String filename) {
		// TODO Auto-generated method stub
			File fname = new File(filename.trim());
			String name = fname.getName();
		return name;
	}
		
  //从XMl文件中读取内容
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
	 //导入csv文件
    public void importCsv()  {
        List<String> dataList=CSVUtils.importCsv(new File("D:"+File.separator+"q.csv"));
        if(dataList!=null && !dataList.isEmpty()){
            for(String data : dataList){
                System.out.println(data);
            }
        }
    }
    //获取某文件夹下所有文件及子文件名称
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

